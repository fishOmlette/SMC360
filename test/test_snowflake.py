import os, json
from unittest.mock import MagicMock, call
from smc360.services.database.snowflake import connection, credentials

dummy_env ={'user': 'user', 'password': 'password', 'account': 'account', 'warehouse': 'warehouse', 'database': 'database', 'schema': 'schema'}

def test_create_or_update_table():
    # Create a mock cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Create a mock credentials object
    mock_credentials = credentials()
    mock_credentials.user = "test_user"
    mock_credentials.password = "test_password"
    mock_credentials.account = "test_account"
    mock_credentials.warehouse = "test_warehouse"
    mock_credentials.database = "test_database"
    mock_credentials.schema = "test_schema"

    # Create a mock table name and column names
    table_name = "test_table"
    column_names = ["col1", "col2", "col3"]

    # Create a mock existing columns list (TIMESTAMP and COL1 already exist)
    mock_cursor.fetchall.return_value = [("TIMESTAMP",), ("COL1",)]

    # Create a mock connection object and call create_or_update_table
    conn = connection()
    conn.conn = mock_conn
    conn.cur = mock_cursor
    conn.create_or_update_table(table_name, column_names)

    # Assert that execute was called 4 times (CREATE, DESCRIBE, 2 ALTER)
    assert mock_cursor.execute.call_count == 4
    
    # First call should be CREATE TABLE with quoted identifiers
    first_call_sql = str(mock_cursor.execute.call_args_list[0][0][0])
    assert '"test_table"' in first_call_sql
    assert 'CREATE TABLE IF NOT EXISTS' in first_call_sql
    
    # Second call should be DESCRIBE with quoted identifier
    second_call_sql = str(mock_cursor.execute.call_args_list[1][0][0])
    assert 'DESCRIBE' in second_call_sql
    assert '"test_table"' in second_call_sql

def test_add_records():
    # Create a mock cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Create a mock credentials object
    mock_credentials = credentials()
    mock_credentials.user = "test_user"
    mock_credentials.password = "test_password"
    mock_credentials.account = "test_account"
    mock_credentials.warehouse = "test_warehouse"
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

    # Assert that executemany was called once
    mock_cursor.executemany.assert_called_once()
    call_args = mock_cursor.executemany.call_args
    
    # Check the SQL contains quoted identifiers
    sql_query = call_args[0][0]
    assert '"test_table"' in sql_query
    assert '"timestamp"' in sql_query
    assert '"col1"' in sql_query
    assert 'INSERT INTO' in sql_query
    
    # Records should be the second argument
    assert call_args[0][1] == records

def test_credentials_class():
    # Initialise
    os.environ['database'] = json.dumps(dummy_env)

    # Test class
    cred = credentials()
    assert cred.user == dummy_env.get('user')
    assert cred.password == dummy_env.get('password')
    assert cred.account == dummy_env.get('account')
    assert cred.warehouse == dummy_env.get('warehouse')
    assert cred.database == dummy_env.get('database')
    assert cred.schema == dummy_env.get('schema')

    del os.environ['database']
