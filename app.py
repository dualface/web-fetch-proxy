#!/usr/bin/env python3
"""
FlareSolverr Adapter Service

Forward GET requests to FlareSolverr running in a container
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FLARESOLVERR_HOST = os.getenv("FLARESOLVERR_HOST", "localhost")
FLARESOLVERR_PORT = int(os.getenv("FLARESOLVERR_PORT", "8191"))
FLARESOLVERR_URL = f"http://{FLARESOLVERR_HOST}:{FLARESOLVERR_PORT}/v1"

PROXY_URL = os.getenv("PROXY_URL", "")


@app.route("/fetch", methods=["GET"])
def fetch():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    try:
        payload = {"cmd": "request.get", "url": url, "maxTimeout": 30000}
        if PROXY_URL:
            payload["proxy"] = {"url": PROXY_URL}
        print(payload)

        response = requests.post(FLARESOLVERR_URL, json=payload, timeout=65)
        data = response.json()

        if data.get("status") == "ok":
            return jsonify(
                {
                    "success": True,
                    "url": url,
                    "status": data.get("solution", {}).get("status"),
                    "headers": data.get("solution", {}).get("headers"),
                    "content": data.get("solution", {}).get("response"),
                }
            )
        else:
            return jsonify(
                {"success": False, "error": data.get("message", "Unknown error")}
            ), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/fetch_contents", methods=["GET"])
def fetch_contents():
    url = request.args.get("url")

    if not url:
        return "Missing url parameter", 400

    try:
        payload = {"cmd": "request.get", "url": url, "maxTimeout": 30000}
        if PROXY_URL:
            payload["proxy"] = {"url": PROXY_URL}

        response = requests.post(FLARESOLVERR_URL, json=payload, timeout=65)
        data = response.json()

        if data.get("status") == "ok":
            return (
                data.get("solution", {}).get("response"),
                200,
                {"Content-Type": "text/plain; charset=utf-8"},
            )
        else:
            return f"Error: {data.get('message', 'Unknown error')}", 500

    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "1803"))
    app.run(host=host, port=port, debug=False)
