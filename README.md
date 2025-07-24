# Moodify - Multi-Service Application

A full-stack application with microservices architecture consisting of:

- **React Client** - Frontend application
- **Django Main Server** - Primary backend service with authentication and core APIs
- **Flask Microservice** - Specialized microservice for specific functionality
- **Express + MongoDB Microservice** - Node.js microservice with MongoDB integration

## Project Structure

```
moodify/
├── client/                     # React frontend application
├── services/
│   ├── main-server/           # Django backend service
│   ├── flask-microservice/    # Flask microservice
│   └── express-microservice/  # Express + MongoDB microservice
├── docker/                    # Docker configurations
├── docs/                      # Project documentation
└── scripts/                   # Build and deployment scripts
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- Docker & Docker Compose
- MongoDB

### Development Setup

1. Clone the repository
2. Set up each service (see individual service READMEs)
3. Use Docker Compose for local development:
   ```bash
   docker-compose up -d
   ```

## Services

### React Client (Port 3000)
- Modern React application with hooks and context
- Responsive design
- API integration with backend services

### Django Main Server (Port 8000)
- Authentication and user management
- Core business logic
- Admin interface
- PostgreSQL database

### Flask Microservice (Port 5000)
- Specialized functionality
- RESTful API
- SQLAlchemy ORM

### Express Microservice (Port 3001)
- MongoDB integration
- Real-time features
- JWT authentication

## Architecture

The application follows a microservices architecture where each service is responsible for specific functionality and can be developed, deployed, and scaled independently.

## Contributing

Please read the contribution guidelines in each service's directory.

## License

This project is licensed under the MIT License.
