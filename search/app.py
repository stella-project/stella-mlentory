import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# STELLA_APP_API = os.environ.get("STELLA_APP_ADDRESS", "http://stella-app:8000") + "/stella/api/v1/"

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("query", "").strip()
    if not query:
        return render_template("home.html", query=query, results=None)
    try:
        response = requests.get("http://app:8000/stella/api/v1/" + "ranking?query=" + query)
        response.raise_for_status()
        results = response.json()
        print(results)
        return render_template("home.html", query=query, results=results)
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)