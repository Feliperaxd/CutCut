
__all__ = ['Pipeline']
__author__ = 'Felipe Amaral'
__version__ = '0.2'

import os 
import sys
import logging
import psycopg2
import traceback
import subprocess

from psycopg2 import sql
from datetime import datetime
from sqlalchemy import create_engine
from contextlib import contextmanager
from psycopg2.extensions import connection
from sqlalchemy.orm import sessionmaker, Session
from typing import (
    Any, Dict, Generator, 
    List, Optional, Union
)

from utils import Utils
from pathlib import Path


class Pipeline:
    """
    Use to make it easier to control the database, 
    allowing the creation of SQLAlchemy sessions or 
    running SQL queries directly through psycopg2.
    """
    

    def __init__(
        self: 'Pipeline'
    ) -> None:
        """
        Attributes:
            - logger (logging.Logger): Logger instance for logging operations.
            - db_user (str): Database user, fetched from environment variables.
            - db_host (str): Database host, fetched from environment variables.
            - db_name (str): Database name, fetched from environment variables.
            - db_port (str): Database port, fetched from environment variables.
            - db_basic (str): Additional database settings, fetched 
                from environment variables.
            - db_password (str): Database password, fetched from environment variables.
            - db_url (str): Formatted database connection URL.
        
            - alchemy_engine (sqlalchemy.engine.base.Engine): SQLAlchemy 
                engine bound to the database URL.
            - SessionFactory (sqlalchemy.orm.session.Session): SQLAlchemy 
                session factory for database operations.
        
            - command_to_dump (list): Command list for backing up the 
                database using `pg_dump`.
            - command_to_restore (list): Command list for restoring the 
                database using `pg_restore`
        """

        self.logger = logging.getLogger('pipeline')
        self.logger.info("'pipeline' logger test!")

        required_vars = [
            'DB_USER', 'DB_HOST', 
            'DB_NAME', 'DB_PORT', 
            'DB_PASSWORD'
        ]
        for var in required_vars:
            if os.getenv(var) is None:
                self.logger.error(f'Environment variable {var} is not set.')
                sys.exit(1)

        # -- To Connect --
        self.db_user = os.getenv('DB_USER')
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_port = os.getenv('DB_PORT')
        self.db_basic = os.getenv('DB_BASIC')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_url = (
            f'postgresql://{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )

        # -- SQL Alchemy --
        self.alchemy_engine = create_engine(self.db_url)
        self.SessionFactory = sessionmaker(
            autoflush=False,
            autocommit=False,  
            bind=self.alchemy_engine
        )
        
        # -- Backup and Restore Commands --
        self.command_to_dump = [
            'pg_dump',                # PostgreSQL backup tool
            '-U', self.db_user,       # Database User
            '-h', self.db_host,       # Database Host
            '-d', self.db_name,       # Name of the database
            '-F', 'c',                # Backup format (custom)
            '-b'                      # Include large binary objects
        ]
        self.command_to_restore = [
            'pg_restore',            # PostgreSQL backup tool
            '-U', self.db_user,      # Database User
            '-h', self.db_host,      # Database Host
            '-d', self.db_name       # Name of the Database
        ]

    @contextmanager
    def session_scope(
        self: 'Pipeline'
    ) -> Generator[Session, None, None]:
        """
        Context manager for SQLAlchemy session.

        Yields:
            - session: A SQLAlchemy session object for database operations.
        
        Automatically commits or rolls back the session and closes it after use.
        """

        session = self.SessionFactory() 
        try:
            yield session  
            session.commit() 

        except Exception as e:
            session.rollback()
            self.logger.error(f"An error occurred. Rolling back the session: {e}")
            raise 

        finally:
            session.close()
        
    def get_connection(
        self: 'Pipeline',
        db_user: Optional[str] = None,
        db_host: Optional[str] = None,
        db_name: Optional[str] = None,
        db_port: Optional[str] = None,
        db_password: Optional[str] = None,
        **kwargs: Dict[str, Any]
    ) -> Optional[connection]:
        """
        Establishes a connection to the PostgreSQL database using the 
        provided parameters or defaults to the class attributes.

        Parameters:
            - db_user (Optional[str]): Database user. Defaults to 'self.db_user' 
                if not provided.
            - db_host (Optional[str]): Database host. Defaults to 'self.db_host' 
                if not provided.
            - db_name (Optional[str]): Database name. Defaults to 'self.db_name' 
                if not provided.
            - db_port (Optional[str]): Database port. Defaults to 'self.db_port'
                if not provided.
            - db_password (Optional[str]): Database password. Defaults to 
                'self.db_password' if not provided.
            **kwargs: Additional parameters for the connection 

        Returns:
            - connection: A connection object to the PostgreSQL database.
            - None: If the connection fails.

        Raises:
            - psycopg2.OperationalError: If the connection fails, an error is 
                logged and the exception is raised.
        """
    
        db_user = db_user or self.db_user
        db_host = db_host or self.db_host
        db_port = db_port or self.db_port
        db_name = db_name or self.db_name
        db_password = db_password or self.db_password

        try:
            return psycopg2.connect(
                user=db_user,
                host=db_host,
                database=db_name,
                port=db_port,
                password=db_password,
                **kwargs
            )
        except psycopg2.OperationalError as e:
            self.logger.error(f"Failed to connect to the database: {e}")
            raise

    def test(
        self: 'Pipeline', 
        **kwargs: Dict[str, Any]
    ) -> bool:
        """
        Tests the database connection by executing a simple query.

        parameters:
            - **kwargs: Additional parameters for the connection (e.g., db_name, etc.).

        Returns:
            - bool: True if the connection is successful, False otherwise.

        Raises:
            - ValueError: If the connection object is None.
            - Exception: For any other issues during the test.
        """

        try:
            with self.get_connection(**kwargs) as connection:
                if connection is None:
                    raise ValueError("Connection object is None.")
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            
            self.logger.info("Database connection test passed.")
            return True

        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False

    def create_backup(
        self: 'Pipeline', 
        file_path: Optional[Union[Path, str]] = None
    ) -> None:
        """
        Create a database backup in specified file path 
        running the 'pg_dump' command.
        
        parameters:
            - file_path (Optional[Union[Path, str]]): Path to save the backup file. 
                If not provided, a default file name is generated using the current date.

        Raises:
            - RuntimeError: If the backup process fails.
        """

        try:
            if file_path is None:
                now = datetime.now()
                file_name = f'backup_{now.strftime("%Y%m%d_%H%M%S")}.bak'
                file_path = Path(file_name)

            file_path = Utils.get_unique_filename(file_path)
            os.environ['PGPASSWORD'] = self.db_password

            command = self.command_to_dump.copy()
            command.extend(['-f', str(file_path)])

            subprocess.run(command, check=True)
            self.logger.info(f"Backup successfully created at: {file_path}")

        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Backup creation failed. Command returned non-zero exit status: {e.returncode}"
            )
            raise RuntimeError(f"Backup creation failed. Error: {e}")

        except Exception as e:
            self.logger.error(
                f"Unexpected error during backup creation: {e}"
            )
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def restore_backup(
        self: 'Pipeline', 
        file_path: Union[Path, str]
    ) -> None:
        """
        Restores a database backup from the specified file path by recreating 
        the database and running the 'pg_restore' command.

        parameters:
            - file_path (Union[Path, str]): The path to the backup file to restore.

        Returns:
            - None: No return value.

        Raises:
            - subprocess.CalledProcessError: If the restore command fails, an 
                exception is raised and logged.
        """
        
        try:
            self.recreate_database()
            os.environ['PGPASSWORD'] = self.db_password

            command = self.command_to_restore.copy()
            command.append(str(file_path))
            self.logger.info(f"Starting the restore process from {file_path}")

            subprocess.run(command, check=True)
            self.logger.info(f"Backup restored successfully from {file_path}")
        
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to restore backup from {file_path}. Error: {e}"
            )
            raise

        except Exception as e:
            self.logger.error(
                f"Unexpected error while restoring backup from {file_path}. Error: {e}"
            )
            raise
    
    def recreate_database(
        self: 'Pipeline'
    ) -> None:
        """
        Recreates the database by dropping it if it exists and 
        then creating it again.

        - Raises:
            Exception: If an error occurs while recreating the database, it's logged.
        """
        
        try:
            self.logger.info(f"Dropping database {self.db_name}...")
            self.run(
                sql_query=f'DROP DATABASE IF EXISTS {self.db_name}',
                db_name=self.db_basic
            )

            self.logger.info(f"Creating database {self.db_name}...")
            self.run(
                sql_query=f'CREATE DATABASE {self.db_name}',
                db_name=self.db_basic
            )

            self.logger.info(f"Database {self.db_name} recreated successfully.")
        
        except Exception as e:
            self.logger.error(f"Error recreating the database {self.db_name}: {e}")
            traceback.print_exc()

    def run(
        self: 'Pipeline', 
        sql_query: Union[sql.Composed, sql.SQL, str],
        **kwargs: Dict[str, Any]
    ) -> List[Any]:
        """
        Executes a given SQL query and returns the result as a list of tuples.

        parameters:
            - sql_query (Union[sql.Composed, sql.SQL, str]): The SQL query to execute.
            - **kwargs: Additional parameters for the connection (e.g., db_name, etc.).

        Returns:
            - List[Any]: A list of query results as tuples, or an empty list 
                if no results.
        
        Raises:
            - Exception: If an error occurs while executing the query, it's 
            - logged and an empty list is returned.
        """
        
        try:
            connection = self.get_connection(**kwargs)
            if connection is None:
                raise
            
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                if cursor.description:
                    return cursor.fetchall()
            return []
        
        except Exception as e:
            self.logger.error(f"Error executing query: {sql_query}. Details: {e}")
            traceback.print_exc()
            return []
        