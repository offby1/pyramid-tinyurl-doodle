import binascii
import hashlib

import pyramid.httpexceptions
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    HashModel,
    )


@view_config(route_name='home', renderer='templates/create.pt', request_method='GET')
def create_GET(request):
    return {'hey': 'this should really be a static view'}

@view_config(route_name='create', request_method='GET')
def create_POST(request):
    session = DBSession()
    try:
        long_url = request.params['input_url']
    except KeyError as e:
        return pyramid.httpexceptions.HTTPBadRequest(e)

    hash_object = hashlib.sha256(long_url)
    binary_hash = hash_object.digest()
    human_hash  = binascii.b2a_base64(binary_hash)[:10]

    new_item = HashModel(human_hash=human_hash,
                         long_url=long_url)
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if not old_item:
        DBSession.add(new_item)
    short_url = '{}/{}'.format(request.application_url, human_hash)
    return Response(body='Dig: <a href="{}">{}</a>'.format(short_url, short_url))


@view_config(route_name='lookup', request_method='GET')
def lookup_GET(request):
    session = DBSession()
    human_hash = request.matchdict['human_hash']
    old_item = session.query(HashModel).filter_by(human_hash=human_hash).first()
    if old_item:
        return pyramid.httpexceptions.HTTPSeeOther(location=old_item.long_url)
    return pyramid.httpexceptions.HTTPNotFound()
