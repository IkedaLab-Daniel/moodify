#!/bin/bash

# Stop all services
echo "Stopping Moodify services..."
docker-compose down

# Remove volumes (optional - uncomment if you want to reset databases)
# docker-compose down -v

echo "Services stopped successfully!"
