from flask import Flask, request, jsonify, redirect
from systems import Ranker


app = Flask(__name__)
ranker = Ranker()


@app.route("/")
def redirect_to_test():
    return redirect("/test", code=302)


@app.route("/test", methods=["GET"])
def test():
    return "Container is running", 200


@app.route("/ranking", methods=["GET"])
def ranking():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter 'query' is required."}), 400

    try:
        page = int(request.args.get("page", 0))
    except ValueError:
        return jsonify({"error": "Parameter 'page' must be an integer."}), 400

    try:
        rpp = int(request.args.get("rpp", 20))
    except ValueError:
        return jsonify({"error": "Parameter 'rpp' must be an integer."}), 400

    try:
        response = ranker.rank_publications(query, page, rpp)
    except Exception as e:
        app.logger.error(f"Error in ranking publications: {e}", exc_info=True)
        return jsonify({"error": "Failed to rank publications."}), 500

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)