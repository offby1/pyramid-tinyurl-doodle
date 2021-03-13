"""
Stuff for using Google's "recaptcha" to keep out spam
https://www.google.com/recaptcha/
"""

# Core
import logging

# Third-party
from IPy import IP              # TODO -- perhaps the built-in ipaddress module will suffice
import requests

logger = logging.getLogger(__name__)


def _authenticated_within_pyramid(request):
    a = request.session.get('authenticated')
    logger.debug("request.session.get('authenticated') => %s", a)
    return a


def is_from_whitelisted_IP(request):
    # TODO -- put the IP address(s) into config

    # the EC2 box on which rudybot runs
    # TODO -- try running `ec2-metadata  --public-ipv4` to get this
    if request.client_addr == '52.8.12.207':
        return True

    # If the client's address is private, that means it's probably me,
    # testing this app.
    i = IP(request.client_addr)
    return i.iptype() in ('PRIVATE', 'LOOPBACK')


def _do_the_google_thang(request):
    response = requests.post(
        url='https://www.google.com/recaptcha/api/siteverify',
        data=dict(
            secret=request.registry.settings.get('recaptcha_secret'),
            response=request.params['g-recaptcha-response'],
            remoteip=request.client_addr,
        ),
    ).json()
    logger.debug("Google's pronouncement: %s", response)
    return response['success']


def _captcha_info_is_valid(request):
    g_captcha_response = request.params.get('g-recaptcha-response')
    if not g_captcha_response:
        return False

    logger.debug("g-recaptcha-response from us: %s", g_captcha_response)

    return _do_the_google_thang(request)


def verify_request(request):
    if is_from_whitelisted_IP(request):
        return True

    if _authenticated_within_pyramid(request):
        return True

    if _captcha_info_is_valid(request):
        logger.info("You just passed the Captcha; now you're authenticated.")
        request.session['authenticated'] = True
        return True

    return False
