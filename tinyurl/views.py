# Core
import logging

# 3rd-party
from pyramid.events import NewRequest, subscriber
from pyramid.exceptions import Forbidden
import pyramid.httpexceptions
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import view_config
import six.moves.urllib.parse
import webob.acceptparse

# Local
from . import auth
from .module import dynamo, hashes


@subscriber(NewRequest)
def stash_ddb_connection(event):
    event.request.database = dynamo.DynamoDB()

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


def _recent_entries(session, request):
    # TODO -- do this right! Duh
    yield dict(
        age=0,
        human_hash='I suppose',
        # TODO -- follow recommendations at
        # http://waitress.readthedocs.org/en/latest/#using-behind-a-reverse-proxy
        # and
        # http://waitress.readthedocs.org/en/latest/#using-paste-s-prefixmiddleware-to-set-wsgi-url-scheme,
        # and use route_url, instead of using route_path: raydeo
        # (Michael Merickel (~raydeo@merickel.org)) says to!
        short_url=request.route_path('lengthen',
                                     human_hash='I really ought to'),
        long_url='actually write this bit')


@view_config(route_name='home', request_method='GET')
def home_GET(request):
    authed = request.session.get('authenticated')
    logger.info("You %s already authenticated.", "are" if authed else "are not")

    return render(request, {
        'recent_entries': _recent_entries('woteva', request),
        'truncate': truncate,
        'display_captcha': not authed
    })


def _is_boss(userid):
    return (userid == 'eric.hanchrow@gmail.com')


def render(request, values):
    accept_header = webob.acceptparse.Accept(str(request.accept))

    if accept_header.best_match(['application/json', 'text/html'
                                 ]) == 'text/html':
        git_info = request.registry.settings['git_info']

        this_commit_url = git_info and '{}commit/{}'.format(
            request.registry.settings['github_home_page'], git_info)
        userid = authenticated_userid(request)
        return render_to_response(
            'templates/homepage.mak',
            dict(
                values,
                github_home_page=request.registry.settings['github_home_page'],
                this_commit_url=this_commit_url,
                userid=userid,
                bossman=_is_boss(userid)),
            request=request)

    r = Response(body=request.application_url + values.get('short_url', ''),
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
    short_url = request.route_path('lengthen', human_hash=human_hash)

    return render(request, {
        'short_url': short_url,
        'recent_entries': _recent_entries('wat', request),
        'truncate': truncate,
    })


@view_config(route_name='lengthen', request_method='GET')
def lengthen_GET(request):
    human_hash = request.matchdict['human_hash']
    old_item = hashes.lengthen_short_string(human_hash, request.database)
    if old_item:
        logger.info("Redirecting to %r", old_item['long_url'])
        return pyramid.httpexceptions.HTTPSeeOther(location=old_item['long_url'])
    return pyramid.httpexceptions.HTTPNotFound()


@view_config(route_name='edit',
             request_method='GET',
             renderer='templates/raw_table.mak')
def edit_GET(request):
    if not _is_boss(authenticated_userid(request)):
        raise Forbidden

    return {'table': []}


@view_config(route_name='delete', request_method='DELETE', renderer='json')
def delete_DELETE(request):
    if not _is_boss(authenticated_userid(request)):
        raise Forbidden

    human_hash = request.matchdict['human_hash']

    victims = []
    for v in victims:
        logger.info("%s: deleting %r", request.client_addr, v)
    victims.delete()
    return "Deleted the row with hash {}".format(human_hash)
