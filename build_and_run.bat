@echo off
REM Script to build and run the microservices architecture

echo Building and running the microservices architecture...

REM Create a Docker network if it doesn't exist
echo Creating Docker network...
docker network create angus-network 2>nul || echo Network already exists

REM Stop and remove existing containers if they exist
echo Stopping and removing existing containers...
docker stop angus-core coral-service angus-db 2>nul || echo No containers to stop
docker rm angus-core coral-service angus-db 2>nul || echo No containers to remove

REM Build the Coral Protocol Service with the fixed Dockerfile
echo Building Coral Protocol Service...
cd coral-service
copy Dockerfile.fixed Dockerfile /Y
docker build -t coral-service .
cd ..

REM Build the Agent Angus Core Service
echo Building Agent Angus Core Service...
cd angus-core
docker build -t angus-core .
cd ..

REM Start the PostgreSQL database
echo Starting PostgreSQL database...
docker run -d ^
  --name angus-db ^
  --network angus-network ^
  -e POSTGRES_USER=angus ^
  -e POSTGRES_PASSWORD=angus ^
  -e POSTGRES_DB=angus ^
  -p 5432:5432 ^
  postgres:14

REM Wait for the database to start
echo Waiting for the database to start...
timeout /t 10 /nobreak > nul

REM Start the Coral Protocol Service
echo Starting Coral Protocol Service...
docker run -d ^
  --name coral-service ^
  --network angus-network ^
  -e CORAL_SERVER_URL=%CORAL_SERVER_URL% ^
  -e DB_HOST=angus-db ^
  -e DB_PORT=5432 ^
  -e DB_USER=angus ^
  -e DB_PASSWORD=angus ^
  -e DB_NAME=angus ^
  -e OPENAI_API_KEY=%OPENAI_API_KEY% ^
  -p 8001:8001 ^
  coral-service

REM Start the Agent Angus Core Service
echo Starting Agent Angus Core Service...
docker run -d ^
  --name angus-core ^
  --network angus-network ^
  -e CORAL_SERVICE_URL=http://coral-service:8001 ^
  -e DB_HOST=angus-db ^
  -e DB_PORT=5432 ^
  -e DB_USER=angus ^
  -e DB_PASSWORD=angus ^
  -e DB_NAME=angus ^
  -e OPENAI_API_KEY=%OPENAI_API_KEY% ^
  -v %cd%\data:/app/data ^
  -v %cd%\uploads:/app/uploads ^
  -v %cd%\input:/app/input ^
  -p 8000:8000 ^
  angus-core

REM Check if the containers are running
echo Checking if the containers are running...
docker ps

echo Microservices architecture is now running!
echo Agent Angus Core Service: http://localhost:8000
echo Coral Protocol Service: http://localhost:8001
