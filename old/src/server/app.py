
__all__ = ['App']
__author__ = 'Felipe Amaral'
__version__ = '0.2'

import logging
import logging.config

from pathlib import Path
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from paths import Paths
from utils import Utils
from api_server import APIServer
from data_service import DataService


class App:
    """
    Main application class for setting up and running the server,
    including logging, background tasks, and API server initialization.
    """


    def __init__(
        self: 'App'
    ) -> None:
        """
        Attributes:
            - config_path (Path): Path to the general configuration JSON file.
            - credentials_path (Path): Path to the credentials environment file.
            - logging_config_path (Path): Path to the logging configuration JSON file.
            - config_data (dict): Loaded configuration data from the JSON file.
            - logging_config_data (dict): Loaded logging configuration data from the 
                JSON file.
            
            - logger (logging.Logger): Logger instance for logging operations.
            - scheduler (BackgroundScheduler): Background scheduler for periodic tasks.
            - api_server (APIServer): Instance of the API server.
            - data_service (DataService): Service instance for data management.
        """

        self.config_path = Paths.CONFIG / 'config.json'
        self.credentials_path = Paths.CONFIG / 'credentials.env'
        self.logging_config_path = Paths.CONFIG / 'logging_config.json'

        self.config_data = Utils.get_data_from_json(self.config_path)
        self.logging_config_data = Utils.get_data_from_json(self.logging_config_path)

        load_dotenv(self.credentials_path)

        self.logger: logging.Logger = None
        self.scheduler = BackgroundScheduler()
        self.api_server: APIServer = None
        self.data_service: DataService = None

    def _setup_logging(
        self: 'App'
    ) -> None:
        """
        Configures the logging system based on the settings in the
        logging configuration JSON file.
        
        Raises:
            - RuntimeError: If the logging configuration cannot be loaded.
        """

        try:
            Path(Paths.LOGS).mkdir(exist_ok=True)
            logging.config.dictConfig(self.logging_config_data)
        
        except Exception as e:
            raise RuntimeError(f'Failed to setup logging: {e}')

        self.logger = logging.getLogger('app')
        self.logger.info("'app' logger test!")

    def _setup_heartbeat(
        self: 'App'
    ) -> None:
        """
        Configures a background job to disable inactive users periodically
        based on the interval specified in the configuration file.
        """
        
        heartbeat_interval = int(
            self.config_data.get('heartbeatCheckInterval', 60)
        )

        self.scheduler.add_job(
            func=self.data_service.disable_inactive_users,
            trigger='interval',
            seconds=heartbeat_interval,
            id='disable_inactive_users',
            name='Disable inactive users',
            replace_existing=True,
        )

    def run(
        self: 'App'
    ) -> None:
        """
        Sets up logging, schedules background tasks, and starts the API server.
        """

        self._setup_logging()

        self.api_server = APIServer()
        self.data_service = DataService()
        self._setup_heartbeat()

        self.scheduler.start()
        self.api_server.run()

        self.logger.info('Server App is running!')


if __name__ == '__main__':
    server_app = App()
    server_app.run()


# --- TODO ---
# Ta salvando 2 acessos assim que cria o usuario
# Pensar em um nome bom
# Criar Carrinho 
# Melhorar o javascript
# Melhorar o Card deixar mais bonito
