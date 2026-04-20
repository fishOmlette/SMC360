import os, json
from unittest.mock import MagicMock, call, ANY
from smc360.services.database.postgresql import connection, credentials

dummy_env = {'user': 'user', 'password': 'password', 'host': 'localhost', 'port': 1234, 'database': 'database', 'schema': 'schema'}

def test_create_or_update_table():
    # Create a mock cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Create a mock credentials object
    mock_credentials = credentials()
    mock_credentials.user = "test_user"
    mock_credentials.password = "test_password"
    mock_credentials.host = "test_host"
    mock_credentials.port = "test_port"
    mock_credentials.database = "test_database"
    mock_credentials.schema = "test_schema"

    # Create a mock table name and column names
    table_name = "test_table"
    column_names = ["col1", "col2", "col3"]

    # Create a mock existing columns list
    mock_cursor.fetchall.return_value = [("timestamp",), ("col1",)]

    # Create a mock connection object and call create_or_update_table
    conn = connection()
    conn.conn = mock_conn
    conn.cur = mock_cursor
    conn.create_or_update_table(table_name, column_names)

    # Assert that execute was called 4 times (CREATE, SELECT, 2 ALTER)
    assert mock_cursor.execute.call_count == 4
    
    # The second call should be the SELECT with parameterized query
    second_call = mock_cursor.execute.call_args_list[1]
    assert 'SELECT column_name FROM information_schema.columns WHERE table_name = %s' in str(second_call)
    assert ('test_table',) in second_call[0]

def test_add_records():
    # Create a mock cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Create a mock credentials object
    mock_credentials = credentials()
    mock_credentials.user = "test_user"
    mock_credentials.password = "test_password"
    mock_credentials.host = "test_host"
    mock_credentials.port = "test_port"
    mock_credentials.database = "test_database"
    mock_credentials.schema = "test_schema"

    # Create a mock table name, column names, and records
    table_name = "test_table"
    column_names = ["col1", "col2", "col3"]
    records = [("2023-05-13 12:00:00", "value1", "value2", "value3"), ("2023-05-13 12:01:00", "value4", "value5", "value6")]

    # Create a mock connection object and call add_records
    conn = connection()
    conn.conn = mock_conn
    conn.cur = mock_cursor
    conn.add_records(table_name, column_names, records)

    # Assert that executemany was called once with records
    mock_cursor.executemany.assert_called_once()
    call_args = mock_cursor.executemany.call_args
    assert call_args[0][1] == records  # Second argument should be records

def test_credentials_class():
    # Initialise
    os.environ['database'] = json.dumps(dummy_env)

    # Test class
    cred = credentials()
    assert cred.user == dummy_env.get('user')
    assert cred.password == dummy_env.get('password')
    assert cred.host == dummy_env.get('host')
    assert cred.port == dummy_env.get('port')
    assert cred.database == dummy_env.get('database')
    assert cred.schema == dummy_env.get('schema')

    del os.environ['database']
