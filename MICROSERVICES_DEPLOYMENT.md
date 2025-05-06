# Microservices Architecture for Agent Angus

This document provides instructions for deploying and using the microservices architecture for Agent Angus, which separates the Coral Protocol integration into its own service to avoid dependency conflicts.

## Architecture Overview

The microservices architecture consists of the following components:

1. **Agent Angus Core Service**
   - Contains the main Agent Angus functionality
   - Handles music analysis, YouTube integration, etc.
   - No direct dependencies on LangChain or Coral Protocol libraries
   - Communicates with Coral Protocol Service via REST API

2. **Coral Protocol Service**
   - Dedicated service for Coral Protocol integration
   - Contains all LangChain dependencies
   - Exposes a simple REST API for the Core Service to use
   - Handles all communication with the Coral Protocol Server

3. **Database Service**
   - Shared database for persistence
   - Used by both Core and Coral Protocol services

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- OpenAI API key

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/angus.git
   cd angus
   ```

2. **Set up environment variables**

   Create a `.env` file in the root directory with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key
   CORAL_SERVER_URL=http://coral.pushcollective.club/sse
   ```

3. **Deploy the services**

   On Linux/macOS:
   ```bash
   chmod +x deploy_microservices.sh
   ./deploy_microservices.sh
   ```

   On Windows:
   ```
   deploy_microservices.bat
   ```

   This will:
   - Build the Docker images for both services
   - Start the containers
   - Run tests to verify that everything is working

4. **Verify the deployment**

   You can check if the services are running with:

   ```bash
   docker-compose -f docker-compose.microservices.yml ps
   ```

   You should see three containers running:
   - angus-core
   - coral-service
   - db

## Testing

### Testing the Coral Protocol Service

You can test the Coral Protocol Service in isolation with:

```bash
docker-compose -f docker-compose.microservices.yml exec coral-service python test_service.py
```

This will:
- Test the health check endpoint
- Register a test agent
- List available agents
- Create a thread
- Send a message

### Testing the Integration

You can test the integration between the Agent Angus Core Service and the Coral Protocol Service with:

```bash
docker-compose -f docker-compose.microservices.yml exec angus-core python test_coral_integration.py
```

This will:
- Test the health check endpoint
- Register a test agent
- List available agents
- Create a thread
- Send a message

## API Documentation

### Coral Protocol Service API

The Coral Protocol Service exposes the following REST API endpoints:

#### Health Check

```
GET /
```

Response:
```json
{
  "status": "ok",
  "message": "Coral Protocol Service is running"
}
```

#### Register Agent

```
POST /agents/register
```

Request:
```json
{
  "agent_name": "agent_name",
  "capabilities": ["capability1", "capability2"]
}
```

Response:
```json
{
  "status": "success",
  "message": "Successfully registered agent 'agent_name' with capabilities: ['capability1', 'capability2']"
}
```

#### Send Message

```
POST /messages/send
```

Request:
```json
{
  "recipient": "recipient_agent",
  "content": "Hello!",
  "thread_id": "optional_thread_id"
}
```

Response:
```json
{
  "status": "success",
  "message": "Successfully sent message to 'recipient_agent'"
}
```

#### List Agents

```
GET /agents/list
```

Response:
```json
{
  "status": "success",
  "agents": [
    {
      "name": "agent1",
      "capabilities": ["capability1", "capability2"]
    },
    {
      "name": "agent2",
      "capabilities": ["capability3"]
    }
  ]
}
```

#### Create Thread

```
POST /threads/create
```

Request:
```json
{
  "participants": ["agent1", "agent2"],
  "initial_message": "Hello!"
}
```

Response:
```json
{
  "status": "success",
  "thread_id": "thread_id",
  "message": "Successfully created thread with participants: ['agent1', 'agent2']"
}
```

## Extending the Architecture

### Adding New Endpoints to the Coral Protocol Service

1. Add a new endpoint to `coral_service/app.py`:

   ```python
   @app.post("/new-endpoint")
   async def new_endpoint(request: NewEndpointRequest):
       # Implementation
       return {"status": "success", "result": "..."}
   ```

2. Add a new method to the client in `angus_core/coral_client.py`:

   ```python
   def new_endpoint(self, param1, param2):
       try:
           response = requests.post(
               f"{self.base_url}/new-endpoint",
               json={"param1": param1, "param2": param2}
           )
           response.raise_for_status()
           return response.json()
       except Exception as e:
           logger.error(f"Failed to call new endpoint: {str(e)}")
           raise
   ```

### Adding New Services

To add a new service to the architecture:

1. Create a new directory for the service:

   ```bash
   mkdir -p new_service
   ```

2. Create a `requirements.txt` file for the service:

   ```
   # Dependencies for the new service
   ```

3. Create a `Dockerfile` for the service:

   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8002

   CMD ["python", "app.py"]
   ```

4. Create the main application file:

   ```python
   # app.py for the new service
   ```

5. Add the service to `docker-compose.microservices.yml`:

   ```yaml
   new-service:
     build:
       context: ./new_service
       dockerfile: Dockerfile
     ports:
       - "8002:8002"
     depends_on:
       - db
     environment:
       - DB_HOST=db
       - DB_PORT=5432
       - DB_USER=angus
       - DB_PASSWORD=angus
       - DB_NAME=angus
   ```

## Troubleshooting

### Services Not Starting

If the services fail to start, check the logs:

```bash
docker-compose -f docker-compose.microservices.yml logs
```

Common issues:
- Missing environment variables
- Port conflicts
- Database connection issues

### Connection Issues Between Services

If the services can't communicate with each other:
- Check that the service names in the Docker Compose file match the hostnames used in the code
- Verify that the ports are correctly exposed
- Check that the services are on the same Docker network

### Database Issues

If there are issues with the database:
- Check that the database container is running
- Verify the database credentials
- Check that the database is accessible from the services

## Conclusion

This microservices architecture provides a clean separation of concerns and avoids dependency conflicts between different parts of the application. By isolating the Coral Protocol integration in its own service, we can ensure that the Agent Angus Core Service remains stable and maintainable.
