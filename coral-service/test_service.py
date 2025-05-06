#!/usr/bin/env python3
"""
Test script for the Coral Protocol Service

This script tests the Coral Protocol Service by making requests to its API endpoints.
"""
import os
import sys
import json
import logging
import asyncio
import argparse
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default service URL
DEFAULT_SERVICE_URL = "http://localhost:8001"

async def test_health(base_url):
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{base_url}/")
        response.raise_for_status()
        logger.info(f"Health check successful: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

async def test_register_agent(base_url):
    """Test the register agent endpoint."""
    try:
        response = requests.post(
            f"{base_url}/agents/register",
            json={"agent_name": "test_agent", "capabilities": ["messaging", "coordination"]}
        )
        response.raise_for_status()
        logger.info(f"Agent registration successful: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"Agent registration failed: {str(e)}")
        return False

async def test_list_agents(base_url):
    """Test the list agents endpoint."""
    try:
        response = requests.get(f"{base_url}/agents/list")
        response.raise_for_status()
        logger.info(f"List agents successful: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"List agents failed: {str(e)}")
        return False

async def test_create_thread(base_url):
    """Test the create thread endpoint."""
    try:
        response = requests.post(
            f"{base_url}/threads/create",
            json={"participants": ["test_agent", "another_agent"], "initial_message": "Hello!"}
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Create thread successful: {result}")
        return result.get("thread_id")
    except Exception as e:
        logger.error(f"Create thread failed: {str(e)}")
        return None

async def test_send_message(base_url, thread_id=None):
    """Test the send message endpoint."""
    try:
        data = {
            "recipient": "another_agent",
            "content": "Hello from test script!"
        }
        
        if thread_id:
            data["thread_id"] = thread_id
            
        response = requests.post(
            f"{base_url}/messages/send",
            json=data
        )
        response.raise_for_status()
        logger.info(f"Send message successful: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"Send message failed: {str(e)}")
        return False

async def run_tests(base_url):
    """Run all tests."""
    logger.info(f"Testing Coral Protocol Service at {base_url}")
    
    # Test health check
    if not await test_health(base_url):
        logger.error("Health check failed, aborting tests")
        return False
        
    # Test register agent
    if not await test_register_agent(base_url):
        logger.error("Agent registration failed, aborting tests")
        return False
        
    # Test list agents
    if not await test_list_agents(base_url):
        logger.error("List agents failed, aborting tests")
        return False
        
    # Test create thread
    thread_id = await test_create_thread(base_url)
    if not thread_id:
        logger.error("Create thread failed, aborting tests")
        return False
        
    # Test send message
    if not await test_send_message(base_url, thread_id):
        logger.error("Send message failed, aborting tests")
        return False
        
    logger.info("All tests passed!")
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test the Coral Protocol Service")
    parser.add_argument("--url", default=DEFAULT_SERVICE_URL, help="Base URL of the service")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Run the tests
    success = asyncio.run(run_tests(args.url))
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)
