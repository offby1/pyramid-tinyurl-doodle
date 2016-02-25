"""
Stuff for using Google's "recaptcha" to keep out spam
https://www.google.com/recaptcha/
"""

import logging
import os
import requests

logger = logging.getLogger(__name__)

_g_recaptcha_secret = None


def recaptcha_secret():
    global _g_recaptcha_secret
    if _g_recaptcha_secret is None:
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, '.recaptcha_secret')) as inf:
            logger.info("Read recaptcha_secret from %s", inf.name)
            _g_recaptcha_secret = inf.read()

    return _g_recaptcha_secret


def _is_whitelisted(client_addr):
    return client_addr == '52.8.12.207'  # the EC2 box on which rudybot runs


def verify_request(request):
    """Returns True if the REQUEST came from a whitelisted IP address
    (i.e., rudybot), or if Google says the request probably came from
    a human.

    """
    client_addr = request.client_addr
    if _is_whitelisted(client_addr):
        return True

    g_recaptcha_response = request.params['g-recaptcha-response']
    logger.debug("g-recaptcha-repsonse from us: %s",
                 request.params['g-recaptcha-response'])

    response = requests.post(
        url='https://www.google.com/recaptcha/api/siteverify',
        data=dict(secret=recaptcha_secret(),
                  response=g_recaptcha_response,
                  remoteip=client_addr)).json()

    logger.debug("Google's pronouncement: %s", response)
    return response['success']
