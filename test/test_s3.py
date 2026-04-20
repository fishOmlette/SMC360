import boto3, os, json
from moto import mock_aws
from smc360.services.object_storage.s3 import connection, credentials

bucket_name = 'test-bucket'
dummy_env ={'endpoint_url': 'localhost:1234', 'aws_access_key_id': 'access_key_id', 'aws_secret_access_key': 'secret_access_key', 'bucket_name': 'bucket_name'}

@mock_aws
def test_read_file():
    # Initialize
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=bucket_name)
    file_name, file_contents = 'test.txt', 'This is test file'
    obj = s3.Object(bucket_name, file_name)
    obj.put(Body=file_contents)

    # Test method
    conn = connection()
    conn.bucket_name = bucket_name
    returned_contents = conn.read_file(file_name)
    assert returned_contents == file_contents

@mock_aws
def test_add_file():
    # Initialize
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=bucket_name)
    file_name, file_contents = 'test.txt', 'This is a test file'

    # Test method
    conn = connection()
    conn.bucket_name = bucket_name
    conn.add_file(file_name, file_contents)
    all_keys = conn.get_objects()
    returned_contents = conn.read_file(file_name)
    assert returned_contents == file_contents
    assert file_name in all_keys

@mock_aws
def test_get_objects():
    # Initialize
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=bucket_name)
    file_keys = ['test1.txt', 'test/test2.txt']

    # Test method
    conn = connection()
    conn.bucket_name = bucket_name
    for file_key in file_keys:
        conn.add_file(file_key, 'sample data')
    all_keys = conn.get_objects()
    assert all_keys.sort() == file_keys.sort()

def test_credentials_class():
    # Initialise
    os.environ['object_storage'] = json.dumps(dummy_env)

    # Test class
    cred = credentials()
    assert cred.endpoint_url == "http://" + dummy_env.get('endpoint_url')
    assert cred.aws_access_key_id == dummy_env.get('aws_access_key_id')
    assert cred.aws_secret_access_key == dummy_env.get('aws_secret_access_key')
    assert cred.bucket_name == dummy_env.get('bucket_name')

    del os.environ['object_storage']
