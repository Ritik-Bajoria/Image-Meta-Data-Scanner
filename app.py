import os
import sys
from utils.extractor import *
from utils.logger import Logger
from flask import Flask, jsonify
from flask_cors import CORS
import signal

logger=Logger()

# Middleware: before each request
@app.before_request
def before_request_func():
    # This will run before every request
    logger.info(f"Request from {request.remote_addr} at {request.method} {request.url}")

# Error response in case of route not found
@app.errorhandler(404)
def not_found_error(e):
    return jsonify({
        "error": True,
        "message": "URL not found"
    }), 404

# Error response in case of method not allowed
@app.errorhandler(405)
def method_not_allowed_error(e):
    return jsonify({
        "error": True,
        "message": "Method not allowed"
    }), 405

@app.route("/api/metadata", methods=['POST'])
def get_meta_data():
# Get the image file from the request
    if 'file' not in request.files:
        return jsonify({
            "error": True,
            'message': 'No file part in the request'
        }), 400

# Graceful shutdown function
def graceful_shutdown(signal, frame):
    logger.info("Shutting down gracefully...")
    # Perform any cleanup here if needed
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    app.run(debug=True,host=host,port=port)
    logger.infot(f"server is listenting at {host}:{port}")
