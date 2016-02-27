# Core
import datetime
import os
import random
import re
import string

# 3rd-party
import babel.dates
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import six
from six.moves import reload_module
from sqlalchemy import engine_from_config

from .models import (DBSession, Base, )


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    expanded = dict((key, os.path.expandvars(value))
                    for key, value in six.iteritems(settings))
    # Kludge-o-rama: sqlalchemy fails with
    # sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres.pg8000
    # if we don't do this.
    if 'sqlalchemy.url' in expanded:
        expanded['sqlalchemy.url'] = re.sub(r'^postgres://',
                                            'postgresql+pg8000://',
                                            expanded['sqlalchemy.url'])

    return expanded


def _grab_git_info():
    try:
        with open('.git-post-checkout-info') as inf:
            for index, line in enumerate(inf):
                if index == 1:
                    return line.rstrip()
    except IOError as e:
        print('{} -- ignoring'.format(e))
        return None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Work around https://github.com/mitsuhiko/babel/issues/137
    try:
        babel.dates.format_timedelta(datetime.timedelta(0))
    except AttributeError:
        os.environ['LC_ALL'] = 'C'
        reload_module(babel.dates)

    settings = expandvars_dict(settings)

    settings['git_info'] = _grab_git_info()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    my_session_factory = SignedCookieSessionFactory(''.join([random.choice(string.ascii_letters) for _ in range (20)]))
    config.set_session_factory(my_session_factory)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('robots', '/robots.txt')
    config.add_route('home', '/')

    # The trailing - ensures that no human_hash will be spelled the
    # same way.
    config.add_route('shorten', '/shorten-/')

    config.add_route('edit', '/edit')
    config.add_route('lengthen', '/{human_hash}', request_method='GET')
    config.add_route('delete', '/{human_hash}', request_method='DELETE')
    config.scan()
    return config.make_wsgi_app()
