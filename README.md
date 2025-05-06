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
├── build_and_run.sh          # Build and run script for Linux/macOS
├── build_and_run.bat         # Build and run script for Windows
├── README.md                 # This file
├── coral-service/            # Coral Protocol Service
│   ├── Dockerfile            # Docker configuration
│   ├── Dockerfile.fixed      # Fixed Docker configuration for dependency conflicts
│   ├── requirements.txt      # Dependencies
│   ├── app.py                # FastAPI application
│   └── test_service.py       # Test script
└── angus-core/               # Agent Angus Core Service
    ├── Dockerfile            # Docker configuration
    ├── requirements.txt      # Dependencies
    ├── app.py                # Flask application
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
   git clone https://github.com/MarkAustinGrow/angus-microservices.git
   cd angus-microservices
   ```

2. **Set up environment variables**

   Create a `.env` file in the root directory with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key
   CORAL_SERVER_URL=http://coral.pushcollective.club/sse
   ```

3. **Build and run the services**

   On Linux/macOS:
   ```bash
   chmod +x build_and_run.sh
   ./build_and_run.sh
   ```

   On Windows:
   ```
   build_and_run.bat
   ```

   This will:
   - Create a Docker network
   - Build the Docker images for both services
   - Start the containers
   - Set up the necessary connections between services

4. **Verify the deployment**

   You can check if the services are running with:

   ```bash
   docker ps
   ```

   You should see three containers running:
   - angus-core
   - coral-service
   - angus-db

## Accessing the Services

Once the services are running, you can access them at:

- Agent Angus Core Service: http://localhost:8000
- Coral Protocol Service: http://localhost:8001

## Troubleshooting

### Dependency Conflicts

If you encounter dependency conflicts when building the Coral Protocol Service, the `build_and_run.sh` and `build_and_run.bat` scripts use a fixed Dockerfile (`Dockerfile.fixed`) that installs dependencies in a specific order to avoid conflicts.

### Container Issues

If you need to stop the containers, you can use:

```bash
docker stop angus-core coral-service angus-db
docker rm angus-core coral-service angus-db
```

### Logs

To view the logs for a specific container:

```bash
docker logs angus-core
docker logs coral-service
docker logs angus-db
```

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
