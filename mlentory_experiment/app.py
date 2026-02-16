from flask import Flask, request, jsonify, redirect
from systems import Ranker


app = Flask(__name__)
ranker = Ranker()


@app.route("/test", methods=["GET"])
def test():
    """Returns a JSON message indicating the container is running."""
    return jsonify({"message": "Container is running"}), 200

@app.route("/<path:url>", methods=["GET"])
def proxy(url):
    """Proxy requests to the appropriate endpoint.
    
    The url parameter contains the base URL path forwarded by STELLA.
    Example: if STELLA receives /proxy/backend:8000/models, it forwards "backend:8000/models" here.
    """
    # Ranking
    try:
        # Pass the base URL path and query parameters to ranker
        response = ranker.rank_publications(url, request.args)
    except Exception as e:
        app.logger.error(f"Error in ranking publications: {e}", exc_info=True)
        return jsonify({"error": "Failed to rank publications."}), 500

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)