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

@view_config(route_name='create', request_method='POST')
def create_POST(request):
    session = DBSession()
    try:
        long_url = request.params['input_url']
    except KeyError as e:
        return pyramid.httpexceptions.HTTPBadRequest(e)

    hash = hashlib.sha256(long_url).digest()

    new_item = HashModel(hash=hash, long_url=long_url)
    old_item = session.query(HashModel).filter_by(hash=hash).first()
    if not old_item:
        DBSession.add(new_item)
    return Response(body=str(new_item))
