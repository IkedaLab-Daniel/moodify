# Python Virtual Environments Setup Guide

## 🎯 **Recommended Structure**

```
services/
├── flask-microservice/
│   ├── venv/              # Flask-specific virtual environment
│   ├── app.py
│   ├── models.py
│   └── requirements.txt
│
├── main-server/
│   ├── venv/              # Django-specific virtual environment
│   ├── manage.py
│   ├── moodify/
│   └── requirements.txt
│
└── express-microservice/   # Node.js (uses npm/yarn, no venv needed)
    ├── package.json
    └── src/
```

## 🚀 **Quick Setup Commands**

### Option 1: Use Our Scripts (Recommended)
```bash
# From project root
./scripts/setup-flask.sh    # Sets up Flask + venv + dependencies
./scripts/setup-django.sh   # Sets up Django + venv + dependencies
```

### Option 2: Manual Setup
```bash
# Flask microservice
cd services/flask-microservice
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Django main server  
cd ../main-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔄 **Daily Development Workflow**

### Flask Service
```bash
cd services/flask-microservice
source venv/bin/activate
python app.py
```

### Django Service
```bash
cd services/main-server
source venv/bin/activate
python manage.py runserver
```

## ✅ **Why Separate Virtual Environments?**

1. **🔒 Dependency Isolation** - No conflicts between Django/Flask packages
2. **📦 Clean Dependencies** - Each service only has what it needs
3. **🚀 Easier Deployment** - Minimal Docker images
4. **👥 Team Development** - Different devs can work independently
5. **🧪 Independent Testing** - Test services in isolation

## 🆚 **Package Version Examples**

**Flask might need:**
- Flask==3.0.0
- SQLAlchemy==1.4.46
- Marshmallow==3.20.1

**Django might need:**
- Django==4.2.7
- SQLAlchemy==2.0.21 (different version!)
- djangorestframework==3.14.0

☠️ **Shared venv = Conflict Hell!**

## 💡 **Pro Tips**

1. **Add venv to .gitignore** (already done)
2. **Use requirements.txt** for each service
3. **Consider pyproject.toml** for modern Python projects
4. **Use Docker** for production (eliminates venv issues)

## 🐳 **Production Note**

In production with Docker, each service gets its own container with its own Python environment, so the separation is even cleaner!
