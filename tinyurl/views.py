# Core
import binascii
import datetime
import hashlib
import logging

# 3rd-party
from    babel.dates import format_timedelta
from    pyramid.exceptions import Forbidden
import  pyramid.httpexceptions
from    pyramid.renderers import render_to_response
from    pyramid.response import Response
from    pyramid.security import authenticated_userid
from    pyramid.view import view_config
import  pytz
import  six.moves.urllib.parse
import  webob.acceptparse

# Local
from .models import (
    DBSession,
    HashModel,
    )

logger = logging.getLogger ('tinyurl')


@view_config(route_name='robots', request_method='GET')
def robots_GET(request):
    r = Response(body="User-agent: *\nDisallow: /\n",
                 status='200 OK')
    r.content_type = 'text/plain'
    return r


def truncate(string, maxlen):
    suffix = '...'
    if len(string) > maxlen:
        return string[:maxlen] + suffix
    return string


def _recent_entries(session, request):
    now = datetime.datetime.now(pytz.utc)

    for e in session.query(HashModel).filter(HashModel.create_date.isnot(None)).order_by(HashModel.create_date.desc()).limit(5):

        # some databases -- such as sqlite -- don't preserve time zone
        # info.  If that's the case, just delete it from now, so as to
        # avoid an exception
        if e.create_date.tzinfo is None:
            now = now.replace(tzinfo = None)

        age = format_timedelta(now - e.create_date)

        yield dict(
            age        = age,
            human_hash = e.human_hash,
            # TODO -- follow recommendations at
            # http://waitress.readthedocs.org/en/latest/#using-behind-a-reverse-proxy
            # and
            # http://waitress.readthedocs.org/en/latest/#using-paste-s-prefixmiddleware-to-set-wsgi-url-scheme,
            # and use route_url, instead of using route_path: raydeo
            # (Michael Merickel (~raydeo@merickel.org)) says to!
            short_url  = request.route_path ('lengthen', human_hash=e.human_hash),
            long_url   = e.long_url
        )


@view_config(route_name='home', request_method='GET')
def home_GET(request):
    session = DBSession()
    return render(request,
                  {
                      'recent_entries': _recent_entries(session, request),
                      'truncate': truncate,
                  })


def _is_boss(userid):
    return (userid == 'eric.hanchrow@gmail.com')


def render(request, values):
    accept_header = webob.acceptparse.Accept(str(request.accept))

    if accept_header.best_match(['application/json', 'text/html']) == 'text/html':
        git_info = request.registry.settings['git_info']

        this_commit_url = git_info and '{}commit/{}'.format(request.registry.settings['github_home_page'], git_info)
        userid = authenticated_userid(request)
        return render_to_response ('templates/homepage.mak',

                                   dict(values,
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
    session = DBSession()
    try:
        long_url = request.params['input_url']
    except KeyError as e:
        return pyramid.httpexceptions.HTTPBadRequest(e)

    if six.moves.urllib.parse.urlparse (long_url).netloc == '':
        long_url = u'http://' + long_url

    # Note that the most-active client of this service
    # (https://github.com/offby1/rudybot/) never submits anything
    # shorter than some threshold; as of this writing that's 75
    # characters.  So as long as the value here is no greater than
    # that, rudybot will keep working.
    if len(long_url) <= 65:
        raise pyramid.httpexceptions.HTTPBadRequest("Are you a spammer?")

    long_url_bytes = long_url.encode('utf-8')
    hash_object = hashlib.sha256(long_url_bytes)
    binary_hash = hash_object.digest()
    human_hash_bytes = binascii.b2a_base64(binary_hash)
    human_hash_bytes = human_hash_bytes.replace(b'+', b'').replace(b'/', b'')[:10]
    human_hash_string = human_hash_bytes.decode('utf-8')

    if not session.query(HashModel).filter_by(human_hash=human_hash_string).first():
        DBSession.add(HashModel(human_hash=human_hash_string,
                                long_url=long_url))

    short_url = request.route_path ('lengthen', human_hash=human_hash_bytes)

    return render(request,
                  {
                      'short_url': short_url,
                      'recent_entries': _recent_entries(session, request),
                      'truncate': truncate,
                  })


@view_config(route_name='lengthen', request_method='GET')
def lengthen_GET(request):
    session = DBSession()
    human_hash = request.matchdict['human_hash']
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if old_item:
        logger.info ("Redirecting to %r", old_item.long_url)
        return pyramid.httpexceptions.HTTPSeeOther(location=old_item.long_url)
    return pyramid.httpexceptions.HTTPNotFound()


@view_config(route_name='edit', request_method='GET', renderer='templates/raw_table.mak')
def edit_GET(request):
    if not _is_boss(authenticated_userid(request)):
        raise Forbidden

    session = DBSession()
    return {'table': session.query(HashModel).all()}


@view_config(route_name='delete', request_method='DELETE', renderer='json')
def delete_DELETE(request):
    if not _is_boss(authenticated_userid(request)):
        raise Forbidden

    session = DBSession()
    human_hash = request.matchdict['human_hash']

    victims = session.query(HashModel).filter_by(human_hash=human_hash)
    for v in victims.all():
        logger.info ("%s: deleting %r", request.client_addr, v)
    victims.delete()
    return "Deleted the row with hash {}".format(human_hash)
