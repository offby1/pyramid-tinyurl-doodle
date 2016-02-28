import unittest
import unittest.mock

from pyramid import testing

from . import auth


class TestRecaptchaStuff(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_missing_URL_parameter(self):
        request = testing.DummyRequest()
        self.assertFalse(auth._captcha_info_is_valid(request))

    def test_Google_says_drop_dead(self):
        request = testing.DummyRequest(params={'g-recaptcha-response': 'yeah yeah whatever'})
        with unittest.mock.patch('tinyurl.auth._do_the_google_thang') as _goog:
            _goog.return_value = False
            self.assertFalse(auth._captcha_info_is_valid(request))

    def test_Google_says_eva_thang_funky(self):
        request = testing.DummyRequest(params={'g-recaptcha-response': 'yeah yeah whatever'})
        with unittest.mock.patch('tinyurl.auth._do_the_google_thang') as _goog:
            _goog.return_value = True
            self.assertTrue(auth._captcha_info_is_valid(request))

    def test_we_only_do_the_google_roundtrip_once(self):
        request = testing.DummyRequest(client_addr='1.2.3.4',
                                       params={'g-recaptcha-response': 'yeah yeah whatever'})
        with unittest.mock.patch('tinyurl.auth._do_the_google_thang') as _goog:
            _goog.return_value = True

            self.assertTrue(auth.verify_request(request))
            self.assertTrue(auth.verify_request(request))

            self.assertEqual(len(_goog.call_args_list), 1)
