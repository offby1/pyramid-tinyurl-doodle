import datetime
import os
import re

import babel.dates
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    expanded = dict((key, os.path.expandvars(value)) for
                    key, value in settings.iteritems())
    # Kludge-o-rama: sqlalchemy fails with
    # sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres.pg8000
    # if we don't do this.
    if 'sqlalchemy.url' in expanded:
        expanded['sqlalchemy.url'] = re.sub(r'^postgres://', 'postgresql+pg8000://', expanded['sqlalchemy.url'])

    return expanded


def _grab_git_info():
    try:
        with open('.git-post-checkout-info') as inf:
            for index, line in enumerate(inf):
                if index == 1:
                    return line.rstrip()
    except IOError as e:
        print(e)
        return None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Work around https://github.com/mitsuhiko/babel/issues/137
    try:
        babel.dates.format_timedelta(datetime.timedelta(0))
    except AttributeError:
        os.environ['LC_ALL'] = 'C'
        reload(babel.dates)

    settings = expandvars_dict (settings)

    settings['git_info'] = _grab_git_info()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # The trailing - ensures that no human_hash will be spelled the
    # same way.
    config.add_route('shorten', '/shorten-/')

    config.add_route('lengthen', '/{human_hash}')
    config.scan()
    return config.make_wsgi_app()
