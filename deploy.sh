#!/bin/bash
# Deployment script for the microservices architecture

# Exit on error
set -e

# Print commands
set -x

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it in the .env file or export it before running this script"
    exit 1
fi

# Check if CORAL_SERVER_URL is set
if [ -z "$CORAL_SERVER_URL" ]; then
    echo "Warning: CORAL_SERVER_URL environment variable is not set"
    echo "Using default value: http://coral.pushcollective.club/sse"
    export CORAL_SERVER_URL="http://coral.pushcollective.club/sse"
fi

# Build and start the containers
echo "Building and starting the containers..."
docker-compose -f docker-compose.microservices.yml down
docker-compose -f docker-compose.microservices.yml build --no-cache
docker-compose -f docker-compose.microservices.yml up -d

# Wait for the services to start
echo "Waiting for services to start..."
sleep 10

# Check if the services are running
echo "Checking if the services are running..."
if docker-compose -f docker-compose.microservices.yml ps | grep -q "Up"; then
    echo "Services are running"
else
    echo "Error: Services failed to start"
    docker-compose -f docker-compose.microservices.yml logs
    exit 1
fi

# Run the tests
echo "Running tests..."
docker-compose -f docker-compose.microservices.yml exec coral-service python test_service.py
docker-compose -f docker-compose.microservices.yml exec angus-core python test_coral_integration.py

echo "Deployment completed successfully!"
