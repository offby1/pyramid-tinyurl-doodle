# Core
import binascii
import hashlib
import logging
import urlparse

# 3rd-party
import pyramid.httpexceptions
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

# Local
from .models import (
    DBSession,
    HashModel,
    )

logger = logging.getLogger ('tinyurl')

# Yeah, yeah, this should probably be a static view.
@view_config(route_name='home', renderer='templates/homepage.pt', request_method='GET')
def home_GET(request):
    return {}

@view_config(route_name='shorten', request_method='GET')
def create_POST(request):
    session = DBSession()
    try:
        long_url = request.params['input_url']
    except KeyError as e:
        return pyramid.httpexceptions.HTTPBadRequest(e)

    # Fail if long_url has no 'netloc'.  Otherwise, when "lengthen"
    # would try to redirect to it, confusing things will happen.
    if urlparse.urlparse (long_url).netloc == '':
        raise pyramid.httpexceptions.HTTPBadRequest("{!r} has no 'netloc'".format (long_url))

    hash_object = hashlib.sha256(long_url)
    binary_hash = hash_object.digest()
    human_hash  = binascii.b2a_base64(binary_hash)[:10].replace('+', '').replace('/', '')

    new_item = HashModel(human_hash=human_hash,
                         long_url=long_url)
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if not old_item:
        DBSession.add(new_item)
    short_url = request.route_url ('lengthen', human_hash=human_hash)
    return Response(body='Dig: <a href="{}">{}</a>'.format(short_url, short_url))


@view_config(route_name='lengthen', request_method='GET')
def lengthen_GET(request):
    session = DBSession()
    human_hash = request.matchdict['human_hash']
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if old_item:
        logger.info ("Redirecting to %r", old_item.long_url)
        return pyramid.httpexceptions.HTTPSeeOther(location=old_item.long_url)
    return pyramid.httpexceptions.HTTPNotFound()
