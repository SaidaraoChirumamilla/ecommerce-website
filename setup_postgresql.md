# PostgreSQL Setup Guide

## Install PostgreSQL

### On macOS:
```bash
# Install using Homebrew
brew install postgresql
brew services start postgresql

# Or install PostgreSQL.app from https://postgresapp.com/
```

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### On Windows:
Download and install from: https://www.postgresql.org/download/windows/

## Create Database and User

1. Connect to PostgreSQL:
```bash
psql postgres
```

2. Create database and user:
```sql
-- Create user
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_password';

-- Create database
CREATE DATABASE ecommerce_db OWNER ecommerce_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Exit PostgreSQL
\q
```

## Alternative: Use Environment Variables

Create a `.env` file in your project root:
```
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_password
DB_HOST=localhost
DB_PORT=5432
```

Then update settings.py to use environment variables:
```python
import os
from pathlib import Path

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ecommerce_db'),
        'USER': os.getenv('DB_USER', 'ecommerce_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'ecommerce_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Run Migrations

After setting up PostgreSQL:

```bash
# Activate virtual environment
source venv/bin/activate

# Make migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Troubleshooting

If you get connection errors:
1. Make sure PostgreSQL is running
2. Check if the database and user exist
3. Verify the credentials in settings.py
4. Check if PostgreSQL is accepting connections on localhost:5432
