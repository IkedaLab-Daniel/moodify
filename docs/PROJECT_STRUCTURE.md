# Project Structure Documentation

## Complete Folder Structure

```
moodify/
├── README.md                           # Main project documentation
├── docker-compose.yml                 # Multi-service orchestration
├── .gitignore                         # Git ignore patterns
├── 
├── client/                            # React Frontend Application
│   ├── package.json                  # React dependencies and scripts
│   ├── public/                       # Static public assets
│   ├── src/                          # React source code
│   │   ├── components/               # Reusable React components
│   │   ├── pages/                    # Page-level components
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── services/                 # API service functions
│   │   ├── utils/                    # Utility functions
│   │   ├── context/                  # React context providers
│   │   └── assets/                   # Images, fonts, etc.
│   ├── Dockerfile                    # React app containerization
│   └── .env                          # Environment variables
│
├── services/                          # Backend Services
│   │
│   ├── main-server/                  # Django Main Backend
│   │   ├── manage.py                 # Django management script
│   │   ├── requirements.txt          # Python dependencies
│   │   ├── moodify/                  # Django project settings
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── apps/                     # Django applications
│   │   │   ├── core/                 # Core functionality
│   │   │   │   ├── models.py
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── urls.py
│   │   │   ├── authentication/       # User authentication
│   │   │   │   ├── models.py
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── urls.py
│   │   │   └── api/                  # API endpoints
│   │   │       ├── views.py
│   │   │       ├── serializers.py
│   │   │       └── urls.py
│   │   ├── config/                   # Configuration files
│   │   ├── static/                   # Static files
│   │   ├── media/                    # Media uploads
│   │   ├── tests/                    # Test files
│   │   ├── Dockerfile                # Django containerization
│   │   └── .env                      # Environment variables
│   │
│   ├── flask-microservice/           # Flask Microservice
│   │   ├── app.py                    # Flask application entry
│   │   ├── requirements.txt          # Python dependencies
│   │   ├── app/                      # Flask application code
│   │   │   ├── __init__.py
│   │   │   ├── api/                  # API routes
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── models/               # Database models
│   │   │   │   ├── __init__.py
│   │   │   │   └── models.py
│   │   │   ├── services/             # Business logic
│   │   │   │   ├── __init__.py
│   │   │   │   └── services.py
│   │   │   └── utils/                # Utility functions
│   │   │       ├── __init__.py
│   │   │       └── helpers.py
│   │   ├── config/                   # Configuration files
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── tests/                    # Test files
│   │   ├── Dockerfile                # Flask containerization
│   │   └── .env                      # Environment variables
│   │
│   └── express-microservice/         # Express + MongoDB Service
│       ├── package.json              # Node.js dependencies
│       ├── src/                      # Express source code
│       │   ├── app.js                # Express application entry
│       │   ├── controllers/          # Request handlers
│       │   │   └── index.js
│       │   ├── models/               # MongoDB models
│       │   │   └── index.js
│       │   ├── routes/               # API routes
│       │   │   └── index.js
│       │   ├── middleware/           # Custom middleware
│       │   │   └── auth.js
│       │   ├── services/             # Business logic
│       │   │   └── index.js
│       │   ├── utils/                # Utility functions
│       │   │   └── helpers.js
│       │   └── config/               # Configuration
│       │       └── database.js
│       ├── tests/                    # Test files
│       ├── Dockerfile                # Express containerization
│       └── .env                      # Environment variables
│
├── docker/                           # Docker Configuration
│   ├── nginx/                        # Nginx configuration
│   │   └── nginx.conf               # Load balancer config
│   ├── postgres/                     # PostgreSQL setup
│   │   └── init-multiple-databases.sh
│   └── mongo/                        # MongoDB setup
│       └── init-mongo.js
│
├── docs/                             # Project Documentation
│   ├── API.md                        # API documentation
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── CONTRIBUTING.md               # Contribution guidelines
│
└── scripts/                          # Build and Deployment Scripts
    ├── start-dev.sh                  # Start development environment
    ├── stop-dev.sh                   # Stop development environment
    ├── build-all.sh                  # Build all services
    └── deploy.sh                     # Production deployment
```

## Service Responsibilities

### React Client (Port 3000)
- User interface and user experience
- State management (React Context/Redux)
- API integration with backend services
- Responsive design and accessibility

### Django Main Server (Port 8000)
- User authentication and authorization
- Core business logic and data models
- Admin interface for content management
- Integration with other microservices
- PostgreSQL database management

### Flask Microservice (Port 5000)
- Specialized functionality (e.g., data processing, analytics)
- Independent database operations
- RESTful API endpoints
- Integration with external services

### Express + MongoDB Microservice (Port 3001)
- Real-time features (WebSocket support)
- Document-based data storage
- Fast data retrieval and caching
- Event-driven architecture

## Development Workflow

1. **Setup**: Use `./scripts/start-dev.sh` to spin up all services
2. **Development**: Each service can be developed independently
3. **Testing**: Run tests in each service directory
4. **Integration**: Services communicate via HTTP APIs
5. **Deployment**: Use Docker Compose for consistent deployments

## Inter-Service Communication

- Services communicate via HTTP REST APIs
- Service discovery through Docker networking
- Shared authentication tokens (JWT)
- Event-driven communication where applicable

## Database Architecture

- **PostgreSQL**: Primary database for Django main server and Flask service
- **MongoDB**: Document store for Express microservice
- **Redis**: Caching and session storage

This structure provides:
- ✅ Clear separation of concerns
- ✅ Independent development and deployment
- ✅ Scalable architecture
- ✅ Consistent development environment
- ✅ Comprehensive documentation
