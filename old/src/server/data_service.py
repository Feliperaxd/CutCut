
__all__ = ['DataService']
__author__ = 'Felipe Amaral'
__version__ = '0.1'

import logging

from datetime import datetime
from sqlalchemy import and_, desc
from typing import Dict, Union, Optional

from utils import Utils
from paths import Paths
from pipeline import Pipeline
from table_controllers import User, Search, Access


class DataService:
    """
    Service for managing system data, including users, searches, and access logs.
    """


    def __init__(self: 'DataService') -> None:
        """
        Attributes:
            - logger (logging.Logger): Logger instance for logging operations.
            - pipe (Pipeline): Database pipeline for managing database sessions and queries.
        """

        self.logger = logging.getLogger('data_service')
        self.logger.info("'data_service' logger test!")
        self.pipe = Pipeline()

    def get_user_data(
        self: 'DataService', 
        **filters: Dict[str, Union[str, int]]
    ) -> Optional[Dict[str, str]]:
        """
        Retrieves user data based on given filters.

        Parameters:
            - **filters (Dict[str, Union[str, int]]): Filters for querying the user, 
                such as `tag`, `id`, etc.

        Returns:
            - Optional[Dict[str, str]]: A dictionary with user data 
                or None if no user is found.

        Raises:
            - Exception: If any error occurs during the operation, it is logged.
        """
        
        try:
            with self.pipe.session_scope() as session:
                query = session.query(User).filter_by(**filters)
                user_data = query.first()

                if user_data:
                    return {
                        column: str(value) for column, value in vars(user_data).items() 
                        if not column.startswith('_')
                    }
                
        except Exception as e:
            self.logger.error(f'Error fetching user data with filters {filters}: {e}')
        return None

    def save_user_data(
        self: 'DataService', 
        tag: str, 
        city: str, 
        region: str, 
        country: str
    ) -> bool:
        """
        Saves a new user's data.

        Parameters:
            - tag (str): User's unique tag.
            - city (str): User's city.
            - region (str): User's region.
            - country (str): User's country.

        Returns:
            - bool: True if the user data is saved successfully, False otherwise.

        Raises:
            - Exception: If an error occurs while saving, it is logged.
        """
        
        try:
            with self.pipe.session_scope() as session:
                new_user = User(tag=tag, city=city, region=region, country=country)
                session.add(new_user)
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving user '{tag}': {e}")
            return False

    def save_search(
        self: 'DataService', 
        query: str, 
        user_id: int, 
        max_results: int
    ) -> bool:
        """
        Saves a new search entry.

        Parameters:
            - query (str): Search query text.
            - user_id (int): ID of the user performing the search.
            - max_results (int): Maximum number of results for the search.

        Returns:
            - bool: True if the search data is saved successfully, False otherwise.

        Raises:
            - Exception: If an error occurs while saving, it is logged.
        """

        try:
            with self.pipe.session_scope() as session:
                new_search = Search(query=query, user_id=user_id, max_results=max_results)
                session.add(new_search)
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving search for user '{user_id}': {e}")
            return False

    def user_heartbeat(
        self: 'DataService', 
        user_id: int
    ) -> bool:
        """
        Updates the last heartbeat for a user, marking them as active.

        Parameters:
            - user_id (int): ID of the user.

        Returns:
            - bool: True if the heartbeat is updated successfully, False otherwise.

        Raises:
            - Exception: If an error occurs while updating the heartbeat, it is logged.
        """

        try:
            with self.pipe.session_scope() as session:
                access = (
                    session.query(Access)
                    .filter_by(user_id=user_id)
                    .order_by(desc(Access.creation_date))
                    .first()
                )
                if access:
                    access.last_heartbeat = datetime.now()
                    access.is_active = True
                    session.add(access)
            return True
        
        except Exception as e:
            self.logger.error(f"Error updating heartbeat for user '{user_id}': {e}")
            return False

    def disable_inactive_users(self: 'DataService') -> bool:
        """
        Disables users who have been inactive for a period exceeding the maximum allowed time.

        Returns:
            - bool: True if inactive users are disabled successfully, False otherwise.

        Raises:
            - Exception: If an error occurs during the operation, it is logged.
        """

        try:
            config_data = Utils.get_data_from_json(
                path=Paths.CONFIG / 'config.json'
            )
            time_ago = Utils.get_time_ago(
                seconds=int(config_data.get('heartbeatMaxTime', 0))
            )

            with self.pipe.session_scope() as session:
                accesses = session.query(Access).filter(
                    and_(
                        Access.last_heartbeat < time_ago,
                        Access.is_active == True
                    )
                )
                accesses.update(
                    {
                        'last_heartbeat': datetime.now(),
                        'is_active': False
                    },
                    synchronize_session=False
                )
            return True
        
        except Exception as e:
            self.logger.error(f'Error while disabling inactive users: {e}')
            return False

    def save_access(
        self: 'DataService', 
        user_id: int
    ) -> bool:
        """
        Records a new access entry for a user.

        Parameters:
            - user_id (int): ID of the user.

        Returns:
            - bool: True if the access is recorded successfully, False otherwise.

        Raises:
            - Exception: If an error occurs while saving the access, it is logged.
        """

        try:
            with self.pipe.session_scope() as session:
                access = Access(user_id=user_id)
                session.add(access)
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving access for user '{user_id}': {e}")
            return False
