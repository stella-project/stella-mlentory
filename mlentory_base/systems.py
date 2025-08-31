import requests
import logging
import json


class Ranker:
    def __init__(self):
        """Initialize the Ranker with the base URL and session."""
        self.timeout = 10  # seconds
        self.base_url = "http://backend:8000/models/search_with_facets"  # Use this when accessing it outside of the container
        # self.base_url = "http://localhost:8000/models/search_with_facets"  # Use this when accessing it from within the container
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)

    def format_response(self, results, query, page, rpp):

        response = {
            # Add pagination metadata at the same level
            "query": query,
            "page": page,
            "rpp": rpp,

            "models": results["models"],
            "total": results["total"], 
            "facets": results.get("facets", {}),
            "facet_config": results.get("facet_config", {})
        }

        return response
    
    def rank_publications(self, query: str, page: int, rpp: int) -> dict:
        """Retrieve ranked publications from the MLentory API based on search criteria.

        Args:
            query (str): The user-provided search query.
            page (int): The starting index for pagination.
            rpp (int): The number of results per page.

        Returns:
            dict: The JSON response from the API, or an error message if the request fails.
        """
        params = {
            "query": query,
        }

        try:
            response = self.session.get(
                self.base_url, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            raw_data = response.json()
            formatted_response = self.format_response(raw_data, query, page, rpp)
            return formatted_response

        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error: {req_err}")
            return {"error": f"Request error: {req_err}"}



# instance = Ranker()
# results = instance.rank_publications("qwen", 0, 20)
# print(results)