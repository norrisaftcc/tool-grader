"""
Webhook Service for Tool Grader

This module provides a Flask web service for handling GitHub webhooks.
"""

import os
import hmac
import hashlib
import json
from flask import Flask, request, jsonify, abort

from autograder.config import get_config
from webhook.handlers import handle_push_event


app = Flask(__name__)


@app.before_request
def validate_webhook():
    """Validate GitHub webhook signature."""
    if request.path != "/webhook/github":
        return
    
    # Skip validation in debug mode if configured
    if app.debug and os.environ.get("SKIP_WEBHOOK_VALIDATION"):
        return
    
    # Get configured secret
    config = get_config()
    webhook_secret = config.get("github_api", "webhook_secret")
    
    if not webhook_secret:
        app.logger.warning("GitHub webhook secret not configured")
        return
    
    # Get signature from headers
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        app.logger.warning("No signature provided in webhook request")
        abort(401, "No signature provided")
    
    # Validate signature
    body = request.get_data()
    computed_hash = hmac.new(
        webhook_secret.encode(), 
        body, 
        hashlib.sha256
    ).hexdigest()
    computed_signature = f"sha256={computed_hash}"
    
    if not hmac.compare_digest(signature, computed_signature):
        app.logger.warning("Invalid webhook signature")
        abort(401, "Invalid signature")


@app.route("/webhook/github", methods=["POST"])
def github_webhook():
    """Handle GitHub webhook events."""
    # Get event type
    event_type = request.headers.get("X-GitHub-Event")
    if not event_type:
        return jsonify({"error": "No event type provided"}), 400
    
    # Get payload
    try:
        payload = request.json
    except:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # Handle push event
    if event_type == "push":
        result = handle_push_event(payload)
        return jsonify(result)
    
    # Acknowledge other events
    return jsonify({
        "status": "acknowledged",
        "event": event_type,
        "message": "Event received but not processed"
    })


@app.route("/webhook/status", methods=["GET"])
def webhook_status():
    """Return webhook service status."""
    return jsonify({
        "status": "ok",
        "message": "Webhook service is running"
    })


if __name__ == "__main__":
    # Set default host and port
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("true", "1", "yes")
    
    app.run(host=host, port=port, debug=debug)