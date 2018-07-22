# Core
import logging
import operator

# 3rd-party
import arrow
from pyramid.exceptions import HTTPForbidden
import pyramid.httpexceptions
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config
import six.moves.urllib.parse
import webob.acceptparse

# Local
from . import auth
from . import helpers
from .db import hashes


logger = logging.getLogger('tinyurl')


@view_config(route_name='robots', request_method='GET')
def robots_GET(request):
    r = Response(body="User-agent: *\nDisallow: /\n", status='200 OK')
    r.content_type = 'text/plain'
    return r


def truncate(string, maxlen):
    suffix = '...'
    if len(string) > maxlen:
        return string[:maxlen] + suffix
    return string


def _recent_entries(request):
    now = arrow.utcnow()

    day_fetcher = request.database.get_one_days_hashes
    for item in helpers.n_most_recent(now, day_fetcher):

        create_date_string = item['create_date']

        # arrow instead of datetime.strptime because of http://bugs.python.org/issue15873
        create_datetime = arrow.get(create_date_string)

        yield dict(
            age = arrow.Arrow.fromdatetime(create_datetime).humanize (other=now),
            human_hash=item['human_hash'],
            short_url=request.route_url('lengthen',
                                        human_hash=item['human_hash']),
            long_url=item['long_url'])


@view_config(route_name='home', request_method='GET')
def home_GET(request):
    authed = request.session.get('authenticated')
    logger.info("You %s already authenticated.", "are" if authed else "are not")

    return render(request, {
        'recent_entries': _recent_entries(request),
        'truncate': truncate,
        'display_captcha': not authed
    })


def _is_boss(request):
    return auth._is_from_whitelisted_IP(request)


def render(request, values):
    try:
        accept_header = webob.acceptparse.AcceptValidHeader(str(request.accept))
    except ValueError as e:
        logger.warn(f'{request.headers["Accept"]!r} is apparently not a valid Accept header: {e}')
    else:
        if accept_header.accepts_html:
            git_info = request.registry.settings['git_info']

            this_commit_url = git_info and '{}commit/{}'.format(
                request.registry.settings['github_home_page'], git_info)
            return render_to_response(
                'templates/homepage.mak',
                dict(
                    values,
                    github_home_page=request.registry.settings['github_home_page'],
                    this_commit_url=this_commit_url,
                    bossman=_is_boss(request)),
                request=request)

    r = Response(body=values.get('short_url', ''),
                 status='200 OK')
    r.content_type = 'text/plain'
    return r


@view_config(route_name='shorten', request_method='GET')
def create_GET(request):
    if not auth.verify_request(request):
        return pyramid.httpexceptions.HTTPUnauthorized(
            body=
            """According to <a href="https://www.google.com/recaptcha/">Google
Recaptcha</a>, you're a robot.  Don't blame me!""")

    try:
        long_url = request.params['input_url']
    except KeyError as e:
        return pyramid.httpexceptions.HTTPBadRequest(e)

    if six.moves.urllib.parse.urlparse(long_url).netloc == '':
        long_url = u'http://' + long_url

    human_hash = hashes.long_url_to_short_string(long_url, request.database)
    short_url = request.route_url('lengthen', human_hash=human_hash)

    body, content_type = render(request, {
        'human_hash': human_hash,
        'short_url': short_url,
        'recent_entries': _recent_entries(request),
        'truncate': truncate,
    })

    return Response(body=body,
                    content_type=content_type,
                    status=200)


@view_config(route_name='lengthen', request_method='GET')
def lengthen_GET(request):
    human_hash = request.matchdict['human_hash']
    try:
        old_item = hashes.lengthen_short_string(human_hash, request.database)
    except KeyError:
        return pyramid.httpexceptions.HTTPNotFound()

    long_url = old_item['long_url']

    # Sort of a development hack: I have lots of items in the database
    # that aren't actually URLs.  Clicking on one of those gets us a
    # 404, so I prepend http: here, simply to make the failure more
    # obvious.
    if not long_url.startswith('http://') and not long_url.startswith('https://'):
        long_url = 'http://{}'.format(long_url)

    logger.info("Redirecting to %r", long_url)
    return pyramid.httpexceptions.HTTPSeeOther(location=long_url)


@view_config(route_name='edit',
             request_method='GET',
             renderer='templates/raw_table.mak')
def edit_GET(request):
    if not _is_boss(request):
        raise HTTPForbidden(detail="Hint: try connecting from a private IP address.")

    return {'table': request.database.get_all()}


@view_config(route_name='delete', request_method='DELETE', renderer='json')
def delete_DELETE(request):
    if not _is_boss(request):
        raise HTTPForbidden

    human_hash = request.matchdict['human_hash']

    logger.info("%s: deleting %r", request.client_addr, human_hash)
    request.database.delete(human_hash)
    return "Deleted the row with hash {}".format(human_hash)
