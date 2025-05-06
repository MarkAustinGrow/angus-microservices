# Angus Microservices Architecture

This repository contains a microservices implementation of Agent Angus, with a specific focus on resolving dependency conflicts in the Coral Protocol integration.

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

## Repository Structure

```
angus-microservices/
├── docker-compose.yml        # Docker Compose configuration
├── deploy.sh                 # Deployment script for Linux/macOS
├── deploy.bat                # Deployment script for Windows
├── README.md                 # This file
├── coral-service/            # Coral Protocol Service
│   ├── Dockerfile            # Docker configuration
│   ├── requirements.txt      # Dependencies
│   ├── app.py                # FastAPI application
│   └── test_service.py       # Test script
└── angus-core/               # Agent Angus Core Service
    ├── Dockerfile            # Docker configuration
    ├── requirements.txt      # Dependencies
    ├── coral_client.py       # Client for Coral Protocol Service
    └── test_coral_integration.py  # Test script
```

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- OpenAI API key

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/angus-microservices.git
   cd angus-microservices
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
   chmod +x deploy.sh
   ./deploy.sh
   ```

   On Windows:
   ```
   deploy.bat
   ```

   This will:
   - Build the Docker images for both services
   - Start the containers
   - Run tests to verify that everything is working

4. **Verify the deployment**

   You can check if the services are running with:

   ```bash
   docker-compose ps
   ```

   You should see three containers running:
   - angus-core
   - coral-service
   - db

## API Documentation

The Coral Protocol Service exposes the following REST API endpoints:

- `GET /` - Health check
- `POST /agents/register` - Register an agent
- `POST /messages/send` - Send a message
- `GET /agents/list` - List available agents
- `POST /threads/create` - Create a new thread

For detailed API documentation, see the [MICROSERVICES_DEPLOYMENT.md](MICROSERVICES_DEPLOYMENT.md) file.

## Benefits of Microservices Architecture

This microservices architecture provides several benefits:

1. **Dependency Isolation**
   - Each service has its own isolated dependencies
   - No conflicts between different package versions
   - Can update each service independently

2. **Scalability**
   - Can scale each service independently based on load
   - Easier to distribute across multiple servers if needed

3. **Maintainability**
   - Clear separation of concerns
   - Easier to update or replace individual components
   - Simplified testing of each component

4. **Resilience**
   - Failure in one service doesn't necessarily affect others
   - Can implement retry mechanisms and circuit breakers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
