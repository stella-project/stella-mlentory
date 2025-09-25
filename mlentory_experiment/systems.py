import random
import logging
import requests
import json

class Ranker:
    def __init__(self):
        """Initialize the Ranker with the base URL and session."""
        self.timeout = 10  # seconds
        self.base_url = "http://backend:8000/models"  # Use this when accessing it outside of the container
        # self.base_url = "http://localhost:8000/models"  # Use this when accessing it from within the container
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)


    def rank_publications(self, url, params) -> dict:
        """
        Retrieve ranked publications from the MLentory API based on search criteria.
        """
        url = f"{self.base_url}/{url}"
        request_params = {**params}
        try:
            response = self.session.get(
                url, params=request_params, timeout=self.timeout
            )
            response.raise_for_status()
            response = response.json()
            return response
            
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error: {req_err}")
            return {"error": f"Request error: {req_err}"}




# params = {"query": "machine learning", "limit": 10, "page": 1}
# instance = Ranker()
# results = instance.rank_publications("search_with_facets", params)
# print(results)