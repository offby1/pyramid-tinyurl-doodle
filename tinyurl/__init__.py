# Core
import logging
import os
import os.path
import re

# 3rd-party
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import six

# Local

from .db import dynamo

logger = logging.getLogger(__name__)


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    expanded = dict(
        (key, os.path.expandvars(value)) for key, value in six.iteritems(settings)
    )

    return expanded


def _grab_git_info():
    try:
        with open('.git-post-checkout-info') as inf:
            for index, line in enumerate(inf):
                if index == 1:
                    return line.rstrip()
    except IOError as e:
        logger.warning('%s -- ignoring', e)
        return None


def _grab_secret(file_name, description):
    file_name = os.path.abspath(file_name)
    try:
        with open(file_name) as inf:
            logger.info("Read %s from %r", description, inf.name)
            return inf.read()
    except (IOError, FileNotFoundError):
        logger.warning("Couldn't read %s %r", description, file_name)
        return ''


def _grab_recaptcha_secret():
    return _grab_secret('.recaptcha_secret', 'recaptcha secret')


def _grab_cookie_secret():
    return _grab_secret('.cookie_secret', 'cookie secret')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # fix logging to be more like RFC3339
    logging.Formatter.default_time_format = '%FT%T'
    logging.Formatter.default_msec_format = '%s.%03dZ'

    settings = expandvars_dict(settings)

    settings['git_info'] = _grab_git_info()
    settings['recaptcha_secret'] = _grab_recaptcha_secret()

    config = Configurator(settings=settings)

    my_session_factory = SignedCookieSessionFactory(_grab_cookie_secret())
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

    table = dynamo.DynamoDB(
        table_name='hashes', daily_index_name='create_day-create_date-index'
    )
    config.add_request_method(lambda request: table, name="database", reify=True)

    config.scan(ignore=[re.compile('test_').search])
    return config.make_wsgi_app()
