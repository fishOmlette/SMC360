import os, json, datetime
import unittest.mock as mock
from smc360.services.platform.instagram import load_to_object_storage, load_to_database, credentials

dummy_env = {'key': 'test-key'}

class MockObjectStorage:
    def connection(self):
        return self

    def add_file(self, file_name, file_contents):
        pass

@mock.patch('requests.get')
def test_users_method(mock_get):
    object_storage = MockObjectStorage()
    expected_user_id = '12345'
    expected_data = {
        'id': expected_user_id,
        'account_type': 'personal',
        'media_count': 10,
        'username': 'johndoe'
    }
    mock_response = mock.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response
    
    obj = load_to_object_storage(object_storage)
    obj.key = 'test-key'
    os.environ['timestamp'] = str(datetime.datetime.now())
    obj.users({})
    
    expected_url = 'https://graph.instagram.com/v16.0/me'
    expected_params = {
        'fields': 'account_type,id,media_count,username',
        'access_token': 'test-key'
    }
    mock_get.assert_called_once_with(expected_url, params=expected_params)
    mock_response.raise_for_status.assert_called_once_with()

@mock.patch('requests.get')
def test_media_method(mock_get):
    object_storage = MockObjectStorage()
    expected_media_id = '12345'
    expected_data = {
        "data": [
      {
        "id": expected_media_id,
        "media_type": "IMAGE",
        "media_url": "https://scontent.cdninstagram.com/...",
        "thumbnail_url": "https://scontent.cdninstagram.com/...",
        "permalink": "https://www.instagram.com/p/B9j8W...",
        "timestamp": "2020-03-10T18:35:17+0000"
      }
    ]
    }
    mock_response = mock.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response
    
    obj = load_to_object_storage(object_storage)
    obj.key = 'test-key'
    os.environ['timestamp'] = str(datetime.datetime.now())
    obj.media({})
    
    expected_url = 'https://graph.instagram.com/v16.0/me/media'
    expected_params = {
        'fields': 'caption,id,is_shared_to_feed,media_type,media_url,permalink,thumbnail_url,timestamp,username,children',
        'access_token': 'test-key',
        'limit': 100
    }
    mock_get.assert_called_once_with(expected_url, params=expected_params)
    mock_response.raise_for_status.assert_called_once_with()

def test_read_parse_load():
    # This test is a placeholder for more comprehensive integration testing
    # The read_parse_load method requires complex mocking of object storage and database
    pass


def test_credentials_class():
    # Initialise
    os.environ['platform'] = json.dumps(dummy_env)

    # Test class
    cred = credentials()
    assert cred.key == dummy_env.get('key')
    assert cred.instagram == 'https://graph.instagram.com/v16.0/'

    del os.environ['platform']
