import sys
from utils.extractor import *
from utils.logger import Logger
from flask import Flask, jsonify, request
from flask_cors import CORS
import signal
import imghdr
from flask_swagger_ui import get_swaggerui_blueprint
import os
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
API_KEY = os.getenv('API_KEY')
print(API_KEY)
logger=Logger()
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
# Connect to MongoDB (default host and port)
client = MongoClient(os.getenv('DB_PATH'))
db = client["image_metadata_db"]  # Choose the database
collection = db["images"] 

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

def validate_api_key():
    # Validate the API key from the request headers.
    api_key = request.headers.get('X-API-KEY')
    if api_key is None or api_key != API_KEY:
        return False
    return True
def convert_objectid_to_string(document):
    """Convert ObjectId in a document to a string for JSON serialization."""
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document

@app.route("/api/metadata", methods=['POST'])
def get_meta_data():
    # Validate the API key
    if not validate_api_key():
        return jsonify({
            "error":True,
            "message": "Unauthorized access"
        }), 401
    
    try:
        # Get the image file from the request
        if 'file' not in request.files:
            return jsonify({
                "error": True,
                'message': 'No file part in the request'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "error": True,
                'message': 'No selected file'
            }), 400
        
        file_type = imghdr.what(file)
        
        if file_type not in ['jpeg', 'jpg', 'png', 'tiff']:
            return jsonify({
                "error": True,
                "message": f"Unsupported file type. Please upload a supported image file."
            }), 400  
        print(file)
        metadata = exif_extractor(file)

        # Add the image name to the metadata
        metadata['image_name'] = file.filename
        # Insert metadata as a document in MongoDB

        result = collection.insert_one(metadata)
        logger.info(f"Metadata for image {file.filename} stored with ID: {result.inserted_id}")
        
        # Convert ObjectId to string before returning or processing further
        stored_metadata = convert_objectid_to_string(metadata)   
        return jsonify(stored_metadata), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

# Graceful shutdown function
def graceful_shutdown(signal, frame):
    logger.info("Shutting down gracefully...")
    # Perform any cleanup here if needed
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == '__main__':
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    app.run(host=host,port=port)
    logger.infot(f"server is listenting at {host}:{port}")
