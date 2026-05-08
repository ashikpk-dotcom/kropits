# KROPITS Deployment Guide for Render

## Prerequisites

1. A [Render](https://render.com) account
2. [PostgreSQL with PostGIS](https://docs.render.com/databases) addon
3. [Redis](https://render.com/docs/redis) addon
4. Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Step-by-Step Deployment

### 1. Push Your Code to Git

```bash
cd kropits
git init
git add .
git commit -m "Initial commit: KROPITS MVP"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:

**Basic Settings:**
- **Name**: `kropits-web`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py makemigrations --noinput && python manage.py migrate --noinput`
- **Start Command**: `gunicorn kropits.wsgi:application -c gunicorn.conf.py`

### 3. Add Environment Variables

In the Render dashboard, go to "Environment" tab and add:

```
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-render-url>.onrender.com
```

Render will automatically add `DATABASE_URL` and `REDIS_URL` when you add the addons.

### 4. Add PostgreSQL Database

1. In Render dashboard, go to "New +" → "PostgreSQL"
2. Create a database with PostGIS extension:
   - **Name**: `kropits-db`
   - **Database Name**: `kropits`
   - **User**: `admin`
   - **Plan**: Free (or paid for production)

3. After creation, go to your web service → "Environment" and add the database:
   - Click "Link Database" and select your `kropits-db`

4. **Important**: Enable PostGIS extension by running this in the Render shell:
   ```bash
   psql $DATABASE_URL -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

### 5. Add Redis

1. Go to "New +" → "Redis"
2. Create a Redis instance:
   - **Name**: `kropits-redis`
   - **Plan**: Free (or paid)

3. Link it to your web service

### 6. Create a Worker Service for Celery

1. Go to "New +" → "Background Worker"
2. Connect the same repository
3. Configure:
   - **Name**: `kropits-worker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A kropits worker -l info`

4. Add the same environment variables as the web service
5. Link the same database and Redis instances

### 7. Deploy Using render.yaml (Alternative)

Alternatively, you can use the included `render.yaml` file for infrastructure-as-code deployment:

1. Push your code with `render.yaml` to your repository
2. In Render dashboard, go to "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and create all services

### 8. Run Migrations

After deployment, you may need to run migrations manually:

1. Go to your web service → "Shell" tab
2. Run:
   ```bash
   python manage.py makemigrations --noinput
   python manage.py migrate --noinput
   ```

### 9. Create Superuser

In the Render shell:
```bash
python manage.py createsuperuser
```

### 10. Verify Deployment

1. Visit your web service URL
2. Check the health endpoint: `https://<your-app>.onrender.com/health/`
3. Test the API endpoints:
   - `POST https://<your-app>.onrender.com/api/auth/register/`
   - `POST https://<your-app>.onrender.com/api/auth/login/`

## Troubleshooting

### Common Issues:

1. **PostGIS not enabled**: Run `CREATE EXTENSION IF NOT EXISTS postgis;` in your database
2. **GDAL/GEOS errors**: The Dockerfile includes these libraries, but Render's native Python environment may not have them. Use Dockerfile-based deploy or ensure buildpack includes them.
3. **Static files not loading**: Check that `whitenoise` is in `requirements.txt` and configured in settings
4. **Celery not connecting to Redis**: Verify `REDIS_URL` environment variable is set correctly

## Monitoring

- Check web service logs in Render dashboard
- Check worker service logs for Celery
- Use `/health/` endpoint for health checks

## Scaling

For production:
- Upgrade to paid plans for database and Redis
- Increase worker count in `gunicorn.conf.py`
- Consider using multiple Celery workers
- Enable autoscaling in Render

## Security Checklist

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is a strong, random value
- [ ] `ALLOWED_HOSTS` includes your Render URL
- [ ] HTTPS is enforced (Render does this automatically)
- [ ] Database credentials are not in code
- [ ] Redis is not publicly accessible
