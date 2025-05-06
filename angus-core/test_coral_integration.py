#!/usr/bin/env python3
"""
Test script for the Agent Angus Core Service's integration with the Coral Protocol Service

This script tests the integration between the Agent Angus Core Service and the Coral Protocol Service
by using the CoralProtocolClient to make requests to the Coral Protocol Service.
"""
import os
import sys
import json
import logging
import argparse
from coral_client import CoralProtocolClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default service URL
DEFAULT_SERVICE_URL = os.getenv("CORAL_SERVICE_URL", "http://localhost:8001")

def test_health_check(client):
    """Test the health check endpoint."""
    try:
        result = client.health_check()
        logger.info(f"Health check successful: {result}")
        return True
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

def test_register_agent(client):
    """Test the register agent endpoint."""
    try:
        result = client.register_agent("angus_test_agent", ["music_analysis", "youtube_integration"])
        logger.info(f"Agent registration successful: {result}")
        return True
    except Exception as e:
        logger.error(f"Agent registration failed: {str(e)}")
        return False

def test_list_agents(client):
    """Test the list agents endpoint."""
    try:
        result = client.list_agents()
        logger.info(f"List agents successful: {result}")
        return True
    except Exception as e:
        logger.error(f"List agents failed: {str(e)}")
        return False

def test_create_thread(client):
    """Test the create thread endpoint."""
    try:
        result = client.create_thread(["angus_test_agent", "another_agent"], "Hello from Angus!")
        logger.info(f"Create thread successful: {result}")
        return result.get("thread_id")
    except Exception as e:
        logger.error(f"Create thread failed: {str(e)}")
        return None

def test_send_message(client, thread_id=None):
    """Test the send message endpoint."""
    try:
        result = client.send_message("another_agent", "Hello from Angus test script!", thread_id)
        logger.info(f"Send message successful: {result}")
        return True
    except Exception as e:
        logger.error(f"Send message failed: {str(e)}")
        return False

def run_tests(service_url):
    """Run all tests."""
    logger.info(f"Testing integration with Coral Protocol Service at {service_url}")
    
    # Create client
    client = CoralProtocolClient(service_url)
    
    # Test health check
    if not test_health_check(client):
        logger.error("Health check failed, aborting tests")
        return False
        
    # Test register agent
    if not test_register_agent(client):
        logger.error("Agent registration failed, aborting tests")
        return False
        
    # Test list agents
    if not test_list_agents(client):
        logger.error("List agents failed, aborting tests")
        return False
        
    # Test create thread
    thread_id = test_create_thread(client)
    if not thread_id:
        logger.error("Create thread failed, aborting tests")
        return False
        
    # Test send message
    if not test_send_message(client, thread_id):
        logger.error("Send message failed, aborting tests")
        return False
        
    logger.info("All tests passed!")
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test integration with Coral Protocol Service")
    parser.add_argument("--url", default=DEFAULT_SERVICE_URL, help="Base URL of the Coral Protocol Service")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Run the tests
    success = run_tests(args.url)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)
