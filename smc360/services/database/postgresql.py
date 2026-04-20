"""
The `postgresql` module provides a `connection` class that can be used to connect to a PostgreSQL database and execute SQL queries. 

The connection is established using a configuration dictionary which should include the following keys:
- `service_name (str)`: The name of the database service to use.
- `user (str)`: The username for authenticating with the database.
- `password (str)`: The password for authenticating with the database.
- `host (str)`: The hostname or IP address of the server where the database is running.
- `port (int)`: The port number on which the database is listening for connections.
- `database (str)`: The name of the database to connect to.
- `schema (str)`: The name of the schema to use within the database.

Example:
----
`database`:
    service_name: postgresql
    user: my-user
    password: my-password
    host: my-host
    port: my-port
    database: my-database
    schema: my-schema

Classes:
----
    - `credentials`: A class that populates credentials
    - `connection`: A context manager that provides a connection to a database and methods for executing SQL queries.
"""

import os
import re
import json
import psycopg2
import logging
from typing import List, Tuple, Any, Optional
from psycopg2 import sql

logger = logging.getLogger(__name__)

# Pattern for valid SQL identifiers (table/column names)
VALID_IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def _validate_identifier(name: str) -> bool:
    """Validate that a name is a safe SQL identifier."""
    return bool(VALID_IDENTIFIER_PATTERN.match(name))

class credentials:
    """
    A class to manage credentials of a database.

    Attributes
    ----
        - `user (str)`: The username for authenticating with the database.
        - `password (str)`: The password for authenticating with the database.
        - `host (str)`: The hostname or IP address of the server where the database is running.
        - `port (int)`: The port number on which the database is listening for connections.
        - `database (str)`: The name of the database to connect to.
        - `schema (str)`: The name of the schema to use within the database.
    """

    def __init__(self):
        env = os.getenv('database')
        cred = json.loads(env) if env is not None else {}
        self.user = cred.get("user")
        self.password = cred.get("password")
        self.host = cred.get("host")
        self.port = cred.get("port")
        self.database = cred.get("database")
        self.schema = cred.get("schema")

class connection(credentials):
    """
    A class to manage connections to a database.

    Attributes
    ----
        - `conn (psycopg2.extensions.connection)`: The connection object.
        - `cur (psycopg2.extensions.cursor)`: The cursor object.

    Methods
    ----
        - `__enter__()`: Establishes a connection to the database and returns the instance.
        - `__exit__(exc_type, exc_value, traceback)`: Closes the connection to the database.
        - `create_or_update_table(table_name, column_names)`: Creates or updates a table in the database.
        - `add_records(table_name, column_names, records)`: Adds records to a table in the database.
    """

    def __init__(self):
        """
        Initializes a new instance of the connection class.
        """

        super().__init__()
        self.conn = None
        self.cur = None
    
    def __enter__(self):
        """
        Establishes a connection to the PostgreSQL database and returns the context manager instance.
        """

        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port, options=f"-c search_path={self.schema}")
        self.cur = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commits or rolls back the transaction and closes the database connection.
        """

        if self.cur is not None:
            try:
                self.cur.close()
            except Exception as e:
                logger.error(str(e))
        if self.conn is not None:
            try:
                if exc_type is not None:
                    self.conn.rollback()
                else:
                    self.conn.commit()
            except Exception as e:
                logger.error(str(e))
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    logger.error(str(e))
    
    def create_or_update_table(self, table_name: str, column_names: List[str]) -> None:
        """
        Creates a new table or updates an existing table in the database with the specified column names.
        
        This method creates a new table with the specified name and columns in the database if it doesn't already exist.
        If the table already exists, it adds any new columns that are specified in the `column_names` parameter to the
        table. If a column with the same name already exists in the table, it is not added again.
        
        Args
        ----
            - `table_name (str)`: The name of the table to create or update.
            - `column_names (list)`: A list of column names to create or add to the table.
        
        Raises
        ----
            - `ValueError`: If table_name or column_names contain invalid characters.
        """
        # Validate identifiers to prevent SQL injection
        if not _validate_identifier(table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        for col in column_names:
            if not _validate_identifier(col):
                raise ValueError(f"Invalid column name: {col}")
        
        # Build CREATE TABLE statement using psycopg2.sql for safe identifier handling
        table_id = sql.Identifier(table_name)
        columns = [sql.SQL("timestamp TIMESTAMP")]
        columns.extend([sql.SQL("{} VARCHAR").format(sql.Identifier(col)) for col in column_names])
        
        create_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            table_id,
            sql.SQL(", ").join(columns)
        )
        self.cur.execute(create_query)
        
        # Get existing columns
        self.cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s;",
            (table_name,)
        )
        existing_columns = [row[0].lower() for row in self.cur.fetchall()]
        
        # Add new columns
        for column_name in column_names:
            if column_name.lower() not in existing_columns:
                alter_query = sql.SQL("ALTER TABLE {} ADD COLUMN {} VARCHAR;").format(
                    table_id,
                    sql.Identifier(column_name)
                )
                self.cur.execute(alter_query)
    
    def add_records(self, table_name: str, column_names: List[str], records: List[Tuple[Any, ...]]) -> None:
        """
        Adds multiple records to the specified table in the database.
        
        This method adds the specified records to the specified table in the database. The `column_names` parameter
        specifies the order of the columns in the database table. The `record` parameter is a list of tuples, where each
        tuple contains the values for one record to be inserted into the table.
        
        Args
        ----
            - `table_name (str)`: The name of the table to create or update.
            - `column_names (list)`: A list of column names to create or add to the table.
            - `records (list)`: A list of tuples, where each tuple represents one record to be inserted into the table.
            The values in the tuple should be in the same order as the column names specified in the `column_names` parameter.
        
        Raises
        ----
            - `ValueError`: If table_name or column_names contain invalid characters.
        """
        # Validate identifiers to prevent SQL injection
        if not _validate_identifier(table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        for col in column_names:
            if not _validate_identifier(col):
                raise ValueError(f"Invalid column name: {col}")
        
        all_columns = ['timestamp'] + column_names
        
        # Build INSERT statement using psycopg2.sql for safe identifier handling
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join([sql.Identifier(col) for col in all_columns]),
            sql.SQL(", ").join([sql.Placeholder()] * len(all_columns))
        )
        self.cur.executemany(insert_query, records)