
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

    def handle_heartbeat(
        self: 'APIServer', 
        user_tag: str
    ) -> Response:
        """
        Handles user heartbeat or access logging based on the request method.

        Parameters:
            - user_tag (str): Unique tag for identifying the user.

        Returns:
            - Response: JSON response indicating whether the operation succeeded.
        """

        user_data = self.data_service.get_user_data(tag=user_tag)
        user_id = user_data.get('id') if user_data else None

        if user_id is None:
            return jsonify({'isSaved': False}), 400

        if request.method == 'PATCH':
            is_saved = self.data_service.user_heartbeat(user_id)

        elif request.method == 'POST':
            is_saved = self.data_service.save_access(user_id)
        
        else:
            return jsonify({'error': 'Invalid request method'}), 405

        return jsonify({'isSaved': is_saved})

    def handle_user_data(
        self: 'APIServer', 
        user_tag: str
    ) -> Response:
        """
        Handles operations on user data (GET or POST).

        Parameters:
            - user_tag (str): Unique tag for identifying the user.

        Returns:
            - Response: JSON response with user data or operation status.
        """
        
        if request.method == 'GET':
            user_data = self.data_service.get_user_data(tag=user_tag)
            if user_data:
                return jsonify(user_data)
            return jsonify({'error': 'User not found'}), 404

        elif request.method == 'POST':
            data = request.json or {}
            is_saved = self.data_service.save_user_data(
                tag=user_tag,
                city=data.get('city', 'Unknown'),
                region=data.get('region', 'Unknown'),
                country=data.get('country', 'Unknown'),
            )
            return jsonify({'isSaved': is_saved})

        return jsonify({'error': 'Invalid request method'}), 405

    def handle_search(
        self: 'APIServer', 
        user_tag: str
    ) -> Response:
        """
        Handles user search queries and processes the results.

        Parameters:
            - user_tag (str): Unique tag for identifying the user.

        Returns:
            - Response: JSON response with search results.
        """

        query_params = request.args.to_dict()
        search_query = query_params.get('query', '')
        max_results = query_params.get('maxResults', 10)
        user_data = self.data_service.get_user_data(tag=user_tag)
        
        if not search_query:
            return jsonify({'error': 'Search query is required'}), 400

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        self.data_service.save_search(
            query=search_query,
            user_id=int(user_data['id']),
            max_results=int(max_results),
        )

        if Utils.is_url(search_query):
            results = self.search_engine.search_by_url(url=search_query)
        
        else:
            results = self.search_engine.search(
                query=search_query, max_results=int(max_results)
            )

        return jsonify({'results': results})

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
