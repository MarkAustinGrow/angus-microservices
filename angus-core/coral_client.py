#!/usr/bin/env python3
"""
Coral Protocol Client

This module provides a client for interacting with the Coral Protocol Service.
It allows the Agent Angus Core Service to communicate with the Coral Protocol
without directly depending on the langchain-mcp-adapters package.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Default Coral service URL
DEFAULT_CORAL_SERVICE_URL = os.getenv("CORAL_SERVICE_URL", "http://coral-service:8001")

class CoralProtocolClient:
    """
    Client for interacting with the Coral Protocol Service.
    
    This client makes HTTP requests to the Coral Protocol Service instead of
    directly using the langchain-mcp-adapters package.
    """
    
    def __init__(self, base_url: str = DEFAULT_CORAL_SERVICE_URL):
        """
        Initialize the Coral Protocol Client.
        
        Args:
            base_url: URL of the Coral Protocol Service
        """
        self.base_url = base_url
        logger.info(f"Initialized Coral Protocol Client with URL: {self.base_url}")
        
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the Coral Protocol Service is running.
        
        Returns:
            Dict: Response from the service
        """
        try:
            response = requests.get(f"{self.base_url}/")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to connect to Coral Protocol Service: {str(e)}")
            raise
            
    def register_agent(self, agent_name: str, capabilities: List[str] = None) -> Dict[str, Any]:
        """
        Register an agent with the Coral Protocol.
        
        Args:
            agent_name: Name of the agent
            capabilities: List of agent capabilities
            
        Returns:
            Dict: Response from the service
        """
        if capabilities is None:
            capabilities = []
            
        try:
            response = requests.post(
                f"{self.base_url}/agents/register",
                json={"agent_name": agent_name, "capabilities": capabilities}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to register agent: {str(e)}")
            raise
            
    def send_message(self, recipient: str, content: str, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message to another agent.
        
        Args:
            recipient: Name of the recipient agent
            content: Message content
            thread_id: Optional thread ID
            
        Returns:
            Dict: Response from the service
        """
        try:
            data = {
                "recipient": recipient,
                "content": content
            }
            
            if thread_id:
                data["thread_id"] = thread_id
                
            response = requests.post(
                f"{self.base_url}/messages/send",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            raise
            
    def list_agents(self, include_details: bool = True) -> Dict[str, Any]:
        """
        List available agents registered with the Coral Protocol.
        
        Args:
            include_details: Whether to include agent details
            
        Returns:
            Dict: Response from the service
        """
        try:
            response = requests.get(
                f"{self.base_url}/agents/list",
                params={"include_details": include_details}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to list agents: {str(e)}")
            raise
            
    def create_thread(self, participants: List[str], initial_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new thread with participants.
        
        Args:
            participants: List of participant agent names
            initial_message: Optional initial message
            
        Returns:
            Dict: Response from the service
        """
        try:
            data = {
                "participants": participants
            }
            
            if initial_message:
                data["initial_message"] = initial_message
                
            response = requests.post(
                f"{self.base_url}/threads/create",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create thread: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Create a client
    client = CoralProtocolClient()
    
    # Check if the service is running
    health = client.health_check()
    print(f"Service health: {health}")
    
    # Register an agent
    result = client.register_agent("test_agent", ["messaging"])
    print(f"Registration result: {result}")
