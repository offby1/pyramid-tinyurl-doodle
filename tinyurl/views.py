# Core
import binascii
import datetime
import hashlib
import logging
import urlparse

# 3rd-party
from babel.dates import format_timedelta
import pyramid.httpexceptions
from pyramid.view import view_config
import pytz

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

    return [dict(
        age        = format_timedelta(now - e.create_date) if e.create_date else '?',
        human_hash = e.human_hash,
        short_url  = request.route_url ('lengthen', human_hash=e.human_hash),
        long_url   = e.long_url
    ) for e in session.query(HashModel).filter(HashModel.create_date.isnot(None)).order_by(HashModel.create_date.desc()).limit(5)]


# Yeah, yeah, this should probably be a static view.
@view_config(route_name='home', renderer='templates/homepage.mak', request_method='GET')
def home_GET(request):
    session = DBSession()
    return {
        'recent_entries': _recent_entries(session, request),
        'truncate': truncate,
    }


@view_config(route_name='shorten', renderer='templates/homepage.mak', request_method='GET')
def create_POST(request):
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

    new_item = HashModel(human_hash=human_hash,
                         long_url=long_url)
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if not old_item:
        DBSession.add(new_item)
    short_url = request.route_url ('lengthen', human_hash=human_hash)

    return {
        'short_url': short_url,
        'recent_entries': _recent_entries(session, request),
        'truncate': truncate,
    }


@view_config(route_name='lengthen', request_method='GET')
def lengthen_GET(request):
    session = DBSession()
    human_hash = request.matchdict['human_hash']
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if old_item:
        logger.info ("Redirecting to %r", old_item.long_url)
        return pyramid.httpexceptions.HTTPSeeOther(location=old_item.long_url)
    return pyramid.httpexceptions.HTTPNotFound()
