#! /usr/bin/env python3
# src/main.py

import os
from flask import Flask, jsonify
from utils.data_object import get_data_object_description
from utils.logger import logger
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/')
def home():
    try:
        logger.info("Received request for home endpoint")
        return "Hello, World!"
    except Exception as e:
        logger.error(f"Error in home endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/object/<string:object_slug>/', defaults={'trailing_slash': True}, strict_slashes=False)
@app.route('/api/object/<string:object_slug>', defaults={'trailing_slash': False}, strict_slashes=False)
def get_object_description(object_slug, trailing_slash):
    """
    Get the description of a data object
    Handles both /api/object/user and /api/object/user/
    """
    try:
        logger.info(f"Received request for object description: {object_slug}")

        # Validate object_slug (basic validation)
        if not object_slug.isalnum() and not all(c in object_slug + '_-' for c in object_slug):
            logger.warning(f"Invalid object slug received: {object_slug}")
            return jsonify({"error": "Invalid object slug"}), 400
            
        data_object = get_data_object_description(object_slug)
        if data_object is None:
            logger.warning(f"Object type not found: {object_slug}")
            return jsonify({"error": "Object type not found"}), 404
            
        logger.info(f"Successfully retrieved object description for: {object_slug}")
        return jsonify(data_object)

    except HTTPException as he:
        # Handle HTTP exceptions (like 404, 405, etc.)
        logger.error(f"HTTP error in get_object_description: {str(he)}")
        return jsonify({"error": str(he)}), he.code

    except Exception as e:
        # Handle any other unexpected errors
        logger.error(f"Unexpected error in get_object_description: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


# Global error handlers
@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"404 error: {str(error)}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        logger.warning(f"HTTP error: {str(e)}")
        return jsonify({"error": str(e)}), e.code

    # Handle non-HTTP errors
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    try:
        # get environment variable HTTP_HOST and HTTP_PORT
        HTTP_HOST = os.environ.get('HTTP_HOST', '0.0.0.0')
        HTTP_PORT = os.environ.get('HTTP_PORT', 1082)
        
        logger.info(f"Starting Flask application on {HTTP_HOST}:{HTTP_PORT}")
        app.run(host=HTTP_HOST, port=HTTP_PORT)
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        raise
