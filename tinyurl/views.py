from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )


@view_config(route_name='home', renderer='templates/create.pt', request_method='GET')
def create_GET(request):
    return {'hey': 'this should really be a static view'}

@view_config(route_name='create', request_method='POST')
def create_POST(request):
    return Response(body=request.params.get('input_url'))
