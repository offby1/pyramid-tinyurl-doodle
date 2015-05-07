# Core
import binascii
import datetime
import hashlib
import logging
import urlparse

# 3rd-party
from    babel.dates import format_timedelta
import  pyramid.httpexceptions
from    pyramid.renderers import render_to_response
from    pyramid.response import Response
from    pyramid.view import view_config
import  pytz
import  webob.acceptparse

# Local
from .models import (
    DBSession,
    HashModel,
    )

logger = logging.getLogger ('tinyurl')

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
            short_url  = request.route_url ('lengthen', human_hash=e.human_hash),
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


def render(request, value):
    accept_header = webob.acceptparse.Accept(str(request.accept))

    if accept_header.best_match(['application/json', 'text/html']) == 'text/html':
        git_info = request.registry.settings['git_info']

        this_commit_url = git_info and '{}commit/{}'.format(request.registry.settings['github_home_page'], git_info)
        return render_to_response ('templates/homepage.mak',

                                   # Stick my beloved git info in there
                                   dict(value,
                                        github_home_page=request.registry.settings['github_home_page'],
                                        this_commit_url=this_commit_url),

                                   request=request)

    r = Response(body=value.get('short_url'),
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

    # Fail if long_url has no 'netloc'.  Otherwise, when "lengthen"
    # would try to redirect to it, confusing things will happen.
    if urlparse.urlparse (long_url).netloc == '':
        raise pyramid.httpexceptions.HTTPBadRequest("{!r} just doesn't look like a proper URL!".format (long_url))

    hash_object = hashlib.sha256(long_url)
    binary_hash = hash_object.digest()
    human_hash  = binascii.b2a_base64(binary_hash).replace('+', '').replace('/', '')[:10]

    if not session.query(HashModel).filter_by(human_hash=human_hash).first():
        DBSession.add(HashModel(human_hash=human_hash,
                                long_url=long_url))

    short_url = request.route_url ('lengthen', human_hash=human_hash)

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
