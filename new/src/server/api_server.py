
__all__ = ['APIServer']
__author__ = 'Felipe Amaral'
__version__ = '0.1'


from flask_cors import CORS
from flask import Flask, request, jsonify, Response

from paths import Paths
from utils import Utils
from data_service import DataService
from search_engine import SearchEngine


class APIServer:
    """
    Handles the Flask application setup, route management, and request processing.
    """


    def __init__(
        self: 'APIServer'
    ) -> None:
        """
        Attributes:
            - self.app (Flask): The Flask application instance
            - self.data_service (DataService): Instance of DataService for managing data.
            - self.search_engine (SearchEngine): Instance of SearchEngine 
                for handling search operations.
        """

        self.app = Flask(__name__)                      
        self.data_service = DataService()
        self.search_engine = SearchEngine()                            

        self._configure_routes()                        
        CORS(self.app)                               

    def _configure_routes(
        self: 'APIServer'
    ) -> None:
        """
        Configures the API routes based on the 'routes.json' configuration file.
        """

        route_file = Paths.CONFIG / 'routes.json'
        routes = Utils.get_data_from_json(route_file)

        for route in routes:
            self.app.add_url_rule(
                rule=route['rule'],
                methods=route['methods'],
                endpoint=route['endpoint'],
                view_func=getattr(self, route['view_func']),
            )

    def run(
        self: 'APIServer',
        is_debug_mode: bool = False
    ) -> None:
        """
        Starts the Flask application server.

        Parameters:
            - is_debug_mode (bool): Indicates whether the server runs in debug mode. 
                Defaults to False. 

        """

        self.app.run(debug=is_debug_mode)
