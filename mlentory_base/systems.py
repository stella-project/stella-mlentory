import requests
import logging
import json


class Ranker:
    def __init__(self):
        """Initialize the Ranker with the base URL and session."""
        self.timeout = 10  # seconds
        self.default_base_url = "http://backend:8000/models"  # Default base URL if not in path
        self.endpoint = "/search_with_facets"  # Endpoint for baseline system
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)


    def rank_publications(self, base_url_path: str, params: dict) -> dict:
        """
        Retrieve ranked publications from the MLentory API based on search criteria.
        
        Args:
            base_url_path: The base URL path from STELLA proxy (e.g., "backend:8000/models")
            params: Query parameters for the search request
        """
        request_params = {**params.copy()}
        
        # STELLA forwards the path after /proxy/ directly, so base_url_path is already "backend:8000/models"

        if base_url_path and not base_url_path.startswith(("http://", "https://")):
            base_url = f"http://{base_url_path}"
        elif base_url_path:
            base_url = base_url_path
        else:
            base_url = self.default_base_url
        
        # Construct full URL: base_url + hardcoded endpoint
        full_url = f"{base_url}{self.endpoint}"

        try:
            response = self.session.get(
                full_url, params=request_params, timeout=self.timeout
            )
            response.raise_for_status()
            response = response.json()
            return response

        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error: {req_err}")
            return {"error": f"Request error: {req_err}"}


# params = {  "query": "machine models", "limit": 10, "page": 1}
# instance = Ranker()
# results = instance.rank_publications(params)
# print(results)