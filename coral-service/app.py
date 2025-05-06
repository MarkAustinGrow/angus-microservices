#!/usr/bin/env python3
"""
Coral Protocol Service

This is the main application file for the Coral Protocol Service.
It provides a REST API for interacting with the Coral Protocol.
"""
import os
import json
import logging
import uuid
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import LangChain and Coral Protocol libraries
try:
    from langchain.agents import AgentExecutor
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain_mcp_adapters.coral_protocol import CoralProtocolClient
    from langchain_mcp_adapters.coral_protocol.models import Agent, Thread
except ImportError:
    logging.warning("LangChain and/or Coral Protocol libraries not installed. Some functionality may be limited.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Coral Protocol Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Coral Protocol Client
coral_client = None
try:
    coral_server_url = os.getenv("CORAL_SERVER_URL", "http://coral.pushcollective.club/sse")
    coral_client = CoralProtocolClient(coral_server_url)
    logger.info(f"Initialized Coral Protocol Client with URL: {coral_server_url}")
except Exception as e:
    logger.error(f"Failed to initialize Coral Protocol Client: {str(e)}")

# Pydantic models for request validation
class RegisterAgentRequest(BaseModel):
    agent_name: str
    capabilities: List[str] = []

class SendMessageRequest(BaseModel):
    recipient: str
    content: str
    thread_id: Optional[str] = None

class CreateThreadRequest(BaseModel):
    participants: List[str]
    initial_message: Optional[str] = None

# Health check endpoint
@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Coral Protocol Service is running"}

# Register agent endpoint
@app.post("/agents/register")
async def register_agent(request: RegisterAgentRequest):
    """Register an agent with the Coral Protocol."""
    if not coral_client:
        raise HTTPException(status_code=500, detail="Coral Protocol Client not initialized")
    
    try:
        agent = Agent(name=request.agent_name, capabilities=request.capabilities)
        coral_client.register_agent(agent)
        return {
            "status": "success",
            "message": f"Successfully registered agent '{request.agent_name}' with capabilities: {request.capabilities}"
        }
    except Exception as e:
        logger.error(f"Failed to register agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to register agent: {str(e)}")

# Send message endpoint
@app.post("/messages/send")
async def send_message(request: SendMessageRequest):
    """Send a message to another agent."""
    if not coral_client:
        raise HTTPException(status_code=500, detail="Coral Protocol Client not initialized")
    
    try:
        message = HumanMessage(content=request.content)
        if request.thread_id:
            coral_client.send_message(request.recipient, message, thread_id=request.thread_id)
        else:
            coral_client.send_message(request.recipient, message)
        return {
            "status": "success",
            "message": f"Successfully sent message to '{request.recipient}'"
        }
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

# List agents endpoint
@app.get("/agents/list")
async def list_agents(include_details: bool = True):
    """List available agents registered with the Coral Protocol."""
    if not coral_client:
        raise HTTPException(status_code=500, detail="Coral Protocol Client not initialized")
    
    try:
        agents = coral_client.list_agents()
        result = []
        for agent in agents:
            if include_details:
                result.append({
                    "name": agent.name,
                    "capabilities": agent.capabilities
                })
            else:
                result.append(agent.name)
        return {
            "status": "success",
            "agents": result
        }
    except Exception as e:
        logger.error(f"Failed to list agents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")

# Create thread endpoint
@app.post("/threads/create")
async def create_thread(request: CreateThreadRequest):
    """Create a new thread with participants."""
    if not coral_client:
        raise HTTPException(status_code=500, detail="Coral Protocol Client not initialized")
    
    try:
        thread_id = str(uuid.uuid4())
        thread = Thread(id=thread_id, participants=request.participants)
        coral_client.create_thread(thread)
        
        if request.initial_message:
            message = HumanMessage(content=request.initial_message)
            for participant in request.participants:
                if participant != request.participants[0]:  # Don't send to the first participant (assumed to be the sender)
                    coral_client.send_message(participant, message, thread_id=thread_id)
        
        return {
            "status": "success",
            "thread_id": thread_id,
            "message": f"Successfully created thread with participants: {request.participants}"
        }
    except Exception as e:
        logger.error(f"Failed to create thread: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create thread: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
