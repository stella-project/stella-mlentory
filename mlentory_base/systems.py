import requests
import logging


class Ranker:
    def __init__(self):
        """Initialize the Ranker with the base URL and session."""
        self.timeout = 10  # seconds
        self.base_url = "http://backend:8000/models/search_by_phrase"  # Use this when accessing it outside of the container
        # self.base_url = "http://localhost:8000/models/search_by_phrase"  # Use this when accessing it from within the container
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)

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
            data = response.json()
            itemlist = [item["db_identifier"] for item in data]
            return {
                "page": page,
                "rpp": rpp,
                "query": query,
                "itemlist": itemlist,
                "num_found": len(itemlist),
            }
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error: {req_err}")
            return {"error": f"Request error: {req_err}"}



# instance = Ranker()
# results = instance.rank_publications("test", 0, 20)
# print(results)