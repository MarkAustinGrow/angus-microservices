@echo off
REM Deployment script for the microservices architecture (Windows version)

echo Starting deployment of microservices architecture...

REM Load environment variables from .env file
if exist .env (
    echo Loading environment variables from .env file
    for /F "tokens=*" %%A in (.env) do set %%A
)

REM Check if OPENAI_API_KEY is set
if "%OPENAI_API_KEY%"=="" (
    echo Error: OPENAI_API_KEY environment variable is not set
    echo Please set it in the .env file or set it before running this script
    exit /b 1
)

REM Check if CORAL_SERVER_URL is set
if "%CORAL_SERVER_URL%"=="" (
    echo Warning: CORAL_SERVER_URL environment variable is not set
    echo Using default value: http://coral.pushcollective.club/sse
    set CORAL_SERVER_URL=http://coral.pushcollective.club/sse
)

REM Build and start the containers
echo Building and starting the containers...
docker-compose -f docker-compose.microservices.yml down
docker-compose -f docker-compose.microservices.yml build --no-cache
docker-compose -f docker-compose.microservices.yml up -d

REM Wait for the services to start
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

REM Check if the services are running
echo Checking if the services are running...
docker-compose -f docker-compose.microservices.yml ps | findstr "Up"
if %ERRORLEVEL% neq 0 (
    echo Error: Services failed to start
    docker-compose -f docker-compose.microservices.yml logs
    exit /b 1
)

REM Run the tests
echo Running tests...
docker-compose -f docker-compose.microservices.yml exec coral-service python test_service.py
docker-compose -f docker-compose.microservices.yml exec angus-core python test_coral_integration.py

echo Deployment completed successfully!
