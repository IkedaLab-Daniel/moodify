#!/bin/bash

# Build and start all services
echo "Building and starting Moodify services..."

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

echo "Services started successfully!"
echo "Client: http://localhost:3000"
echo "Django Main Server: http://localhost:8000"
echo "Flask Microservice: http://localhost:5000"
echo "Express Microservice: http://localhost:3001"
echo ""
echo "To view logs: docker-compose logs -f [service-name]"
echo "To stop services: docker-compose down"
