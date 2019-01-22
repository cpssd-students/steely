#!/usr/bin/env python3


from nose.tools import *
from paths import CONFIG
from steely.plugins  import lastfm
from unittest.mock import patch


@patch('steely.plugins.lastfm.requests.get')
def test_lastfm_api_request(mock_requests_get):
    response = lastfm.get_lastfm_request(
        method='api method', key1='value 1', key2='value 2')
    mock_requests_get.assert_called_once()
    mock_requests_get.assert_called_with(lastfm.API_BASE,
                                         params={'method': 'api method',
                                                 'api_key': CONFIG.LASTFM_API_KEY,
                                                 'format': 'json',
                                                 'key1': 'value 1',
                                                 'key2': 'value 2'})
