# KROPITS - AgriTech Logistics Platform MVP

## Overview
KROPITS is a production-ready agritech logistics platform connecting farmers, buyers, and delivery partners with AI-based matching and route optimization.

## Features
- **Multilingual Support**: English and Malayalam with complete translation
- **Mobile-First UI**: Bootstrap 5 responsive design
- **Role-Based Access**: Farmer, Buyer, Delivery Partner, Admin
- **AI Matching**: Farmer-buyer matching algorithm
- **Route Optimization**: OR-Tools based delivery routing
- **Geospatial Support**: Location-based discovery (PostGIS ready)
- **JWT Authentication**: Secure API access
- **Celery Tasks**: Background job processing
- **Production Ready**: Render cloud deployment

## Tech Stack
- **Backend**: Django 5, Django REST Framework, Celery
- **Database**: PostgreSQL with PostGIS (SQLite for development)
- **Frontend**: Django Templates, Bootstrap 5
- **Optimization**: OR-Tools
- **Authentication**: JWT (SimpleJWT)
- **Deployment**: Render (Web + Worker + Redis + PostgreSQL)

## Project Structure
```
kropits/
├── manage.py
├── kropits/
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── accounts/          # Custom user model, JWT auth
├── farmers/           # Product management
├── buyers/            # Buyer requests, geo-discovery
├── logistics/         # Orders, delivery assignments
├── optimizer/         # AI matching, route optimization
├── adminpanel/        # Admin dashboards
├── templates/         # Bootstrap 5 templates
├── static/           # CSS, JS files
├── locale/           # Translation files (en, ml)
├── render.yaml       # Render deployment config
├── Dockerfile        # Container configuration
└── requirements.txt  # Python dependencies
```

## API Endpoints
### Auth
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh JWT token
- `PATCH /api/auth/set-language/` - Update language preference

### Farmers
- `GET/POST /api/farmers/products/` - List/create products
- `GET/PUT/PATCH/DELETE /api/farmers/products/<id>/` - Product CRUD
- `PATCH /api/farmers/availability/<id>/` - Toggle availability

### Buyers
- `GET/POST /api/buyers/requests/` - List/create requests
- `GET /api/buyers/nearby-farmers/` - Find nearby farmers

### Orders & Delivery
- `POST /api/orders/create/` - Create order
- `GET /api/orders/<id>/status/` - Get order status
- `GET /api/delivery/partners/available/` - List available partners
- `POST /api/delivery/assign/` - Assign delivery
- `PATCH /api/delivery/proof-upload/<id>/` - Upload proof of delivery

### Optimizer
- `POST /api/optimizer/match/` - Match farmers to buyers
- `POST /api/optimizer/route/` - Optimize delivery routes
- `POST /api/optimizer/predict/` - Predict demand

### Health Check
- `GET /health/` - Health check endpoint

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL with PostGIS (for production)
- Redis (for Celery)

### Local Development
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`
8. Access at: http://127.0.0.1:8000

### Environment Variables
Create `.env` file (see `.env.example`):
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Deployment on Render

### Option 1: Using render.yaml (Recommended)
1. Push code to Git repository
2. In Render dashboard, click "New +" → "Blueprint"
3. Connect repository
4. Render will create all services automatically

### Option 2: Manual Setup
1. Create Web Service with build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
2. Start command: `gunicorn kropits.wsgi:application -c gunicorn.conf.py`
3. Add PostgreSQL database with PostGIS extension
4. Add Redis instance
5. Create Worker service for Celery

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

## Testing the API
Use Postman or curl to test endpoints:

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "first_name": "John", "last_name": "Doe", "role": "farmer", "password": "testpass123", "password2": "testpass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "password": "testpass123"}'
```

## Multilingual Support
- Language switcher in navbar
- Translations in `locale/ml/LC_MESSAGES/django.po`
- Compile translations: `python manage.py compilemessages`
- User language preference saved in profile

## Background Tasks (Celery)
Start Celery worker:
```bash
celery -A kropits worker -l info
```

Tasks included:
- Route optimization
- Demand prediction
- Auto delivery assignment

## License
MIT License

## Support
For issues and feature requests, please contact the development team.
