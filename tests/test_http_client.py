import unittest

import httpretty

from pybot.http_client import HttpClient
from pybot.resources.urls import FACEBOOK_MESSAGES_POST_URL


class TestHttpClient(unittest.TestCase):
    """
    Test the HttpClient
    """

    @httpretty.activate
    def test_submit_GET_request(self):

        httpretty.register_uri(httpretty.GET,
            FACEBOOK_MESSAGES_POST_URL + '/users/123',
            body='{ \
                "data" : [1,2,3] \
            }')

        def completion(payload, error):
            assert payload['data'] == [1, 2, 3]
            assert payload['data'] != [3, 2, 1]

        client = HttpClient()
        client.submit_request('/users/123', 'GET', None, completion)

    @httpretty.activate
    def test_submite_POST_request(self):

        httpretty.register_uri(httpretty.POST,
            FACEBOOK_MESSAGES_POST_URL + 'users/',
            body='{ \
                "name": "ben", \
                "age": 12 \
            }', status=201)

        def completion(payload, error):
            
            if error is None:
                assert payload['name'] == 'ben'
                assert payload['age'] == 12
            else:
                raise

        client = HttpClient()
        client.submit_request('users/', 'POST', None, completion)

