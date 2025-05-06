#!/usr/bin/env python3
"""
Agent Angus Core Service

This is the main application file for the Agent Angus Core Service.
It provides a REST API for interacting with the Agent Angus functionality.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from coral_client import CoralProtocolClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Create Coral Protocol Client
coral_client = CoralProtocolClient(os.getenv("CORAL_SERVICE_URL", "http://coral-service:8001"))

@app.route("/")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Agent Angus Core Service is running"
    })

@app.route("/coral/health", methods=["GET"])
def coral_health():
    """Check if the Coral Protocol Service is running."""
    try:
        result = coral_client.health_check()
        return jsonify({
            "status": "ok",
            "coral_service": result
        })
    except Exception as e:
        logger.error(f"Failed to connect to Coral Protocol Service: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to connect to Coral Protocol Service: {str(e)}"
        }), 500

@app.route("/coral/register", methods=["POST"])
def register_agent():
    """Register an agent with the Coral Protocol."""
    data = request.json
    agent_name = data.get("agent_name")
    capabilities = data.get("capabilities", [])
    
    if not agent_name:
        return jsonify({
            "status": "error",
            "message": "Missing required parameter: agent_name"
        }), 400
        
    try:
        result = coral_client.register_agent(agent_name, capabilities)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Failed to register agent: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to register agent: {str(e)}"
        }), 500

@app.route("/coral/send_message", methods=["POST"])
def send_message():
    """Send a message to another agent."""
    data = request.json
    recipient = data.get("recipient")
    content = data.get("content")
    thread_id = data.get("thread_id")
    
    if not recipient:
        return jsonify({
            "status": "error",
            "message": "Missing required parameter: recipient"
        }), 400
        
    if not content:
        return jsonify({
            "status": "error",
            "message": "Missing required parameter: content"
        }), 400
        
    try:
        result = coral_client.send_message(recipient, content, thread_id)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to send message: {str(e)}"
        }), 500

@app.route("/coral/list_agents", methods=["GET"])
def list_agents():
    """List available agents registered with the Coral Protocol."""
    include_details = request.args.get("include_details", "true").lower() == "true"
    
    try:
        result = coral_client.list_agents(include_details)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Failed to list agents: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to list agents: {str(e)}"
        }), 500

@app.route("/coral/create_thread", methods=["POST"])
def create_thread():
    """Create a new thread with participants."""
    data = request.json
    participants = data.get("participants")
    initial_message = data.get("initial_message")
    
    if not participants:
        return jsonify({
            "status": "error",
            "message": "Missing required parameter: participants"
        }), 400
        
    try:
        result = coral_client.create_thread(participants, initial_message)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Failed to create thread: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to create thread: {str(e)}"
        }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
