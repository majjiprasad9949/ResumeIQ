# PostgreSQL Setup Guide for ResumeIQ

This guide provides instructions for setting up PostgreSQL for local development and production environments.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Setup](#production-setup)
3. [Connection Pooling Configuration](#connection-pooling-configuration)
4. [Testing the Connection](#testing-the-connection)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- PostgreSQL 12 or higher
- Python 3.9+
- Django 4.2+

### Windows Setup

#### 1. Install PostgreSQL

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Choose port 5432 (default)
5. Complete the installation

#### 2. Create Database and User

Open PostgreSQL Command Line (psql):

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ai_resume_optimizer;

# Create user
CREATE USER ai_user WITH PASSWORD 'your_secure_password';

# Grant privileges
ALTER ROLE ai_user SET client_encoding TO 'utf8';
ALTER ROLE ai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_user SET default_transaction_deferrable TO on;
ALTER ROLE ai_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE ai_resume_optimizer TO ai_user;

# Exit psql
\q
```

#### 3. Update Environment Variables

Edit `backend/.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=ai_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

### macOS Setup

#### 1. Install PostgreSQL using Homebrew

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify installation
psql --version
```

#### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE ai_resume_optimizer;

# Create user
CREATE USER ai_user WITH PASSWORD 'your_secure_password';

# Grant privileges
ALTER ROLE ai_user SET client_encoding TO 'utf8';
ALTER ROLE ai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_user SET default_transaction_deferrable TO on;
ALTER ROLE ai_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE ai_resume_optimizer TO ai_user;

# Exit psql
\q
```

#### 3. Update Environment Variables

Edit `backend/.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=ai_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

### Linux Setup (Ubuntu/Debian)

#### 1. Install PostgreSQL

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

#### 2. Create Database and User

```bash
# Connect to PostgreSQL as postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE ai_resume_optimizer;

# Create user
CREATE USER ai_user WITH PASSWORD 'your_secure_password';

# Grant privileges
ALTER ROLE ai_user SET client_encoding TO 'utf8';
ALTER ROLE ai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_user SET default_transaction_deferrable TO on;
ALTER ROLE ai_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE ai_resume_optimizer TO ai_user;

# Exit psql
\q
```

#### 3. Update Environment Variables

Edit `backend/.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=ai_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

### 4. Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt

# Verify psycopg2 installation
python -c "import psycopg2; print(f'psycopg2 version: {psycopg2.__version__}')"
```

### 5. Run Django Migrations

```bash
# Navigate to backend directory
cd backend

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

---

## Production Setup

### AWS RDS PostgreSQL Setup

#### 1. Create RDS Instance

1. Go to AWS RDS Console
2. Click "Create database"
3. Select "PostgreSQL"
4. Choose "Production" template
5. Configure:
   - DB instance identifier: `ai-resume-optimizer-prod`
   - Master username: `postgres`
   - Master password: Generate a strong password
   - DB instance class: `db.t3.micro` (or larger for production)
   - Storage: 20 GB (or more as needed)
   - Multi-AZ: Yes (for production)
   - Backup retention: 7 days
6. Create security group allowing inbound traffic on port 5432
7. Create the database

#### 2. Update Production Environment

Create or update `backend/.env.production`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=postgres
DB_PASSWORD=your-rds-master-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

#### 3. Create Application Database and User

```bash
# Connect to RDS instance
psql -h your-rds-endpoint.rds.amazonaws.com -U postgres -d postgres

# Create application database
CREATE DATABASE ai_resume_optimizer;

# Create application user
CREATE USER ai_app WITH PASSWORD 'your_app_password';

# Grant privileges
ALTER ROLE ai_app SET client_encoding TO 'utf8';
ALTER ROLE ai_app SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_app SET default_transaction_deferrable TO on;
ALTER ROLE ai_app SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE ai_resume_optimizer TO ai_app;

# Exit psql
\q
```

#### 4. Update Production Environment

Update `backend/.env.production`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=ai_app
DB_PASSWORD=your_app_password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

---

## Connection Pooling Configuration

### Overview

Connection pooling improves performance by reusing database connections instead of creating new ones for each request.

### Django Configuration

The application uses Django's built-in connection pooling with the following settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_resume_optimizer',
        'USER': 'ai_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Connection lifetime in seconds
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'  # 30 second timeout
        }
    }
}
```

### Configuration Parameters

- **CONN_MAX_AGE**: Maximum age of a connection in seconds (default: 600 = 10 minutes)
  - Set to 0 to disable connection pooling
  - Set to None for unlimited connection lifetime
  - Recommended: 600 seconds for most applications

- **connect_timeout**: Connection timeout in seconds (default: 10)
  - Prevents hanging connections
  - Recommended: 10 seconds

- **statement_timeout**: Query timeout in milliseconds (default: 30000 = 30 seconds)
  - Prevents long-running queries from blocking
  - Recommended: 30000 milliseconds

### Advanced Connection Pooling with PgBouncer

For high-traffic production environments, consider using PgBouncer:

#### 1. Install PgBouncer

**Ubuntu/Debian:**
```bash
sudo apt install pgbouncer
```

**macOS:**
```bash
brew install pgbouncer
```

#### 2. Configure PgBouncer

Edit `/etc/pgbouncer/pgbouncer.ini`:

```ini
[databases]
ai_resume_optimizer = host=localhost port=5432 dbname=ai_resume_optimizer

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 100
max_user_connections = 100
server_lifetime = 3600
server_idle_timeout = 600
```

#### 3. Start PgBouncer

```bash
# Start service
sudo systemctl start pgbouncer
sudo systemctl enable pgbouncer

# Verify
sudo systemctl status pgbouncer
```

#### 4. Update Django Configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_resume_optimizer',
        'USER': 'ai_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',  # PgBouncer host
        'PORT': '6432',       # PgBouncer port
        'CONN_MAX_AGE': 600,
    }
}
```

---

## Testing the Connection

### 1. Run Connection Test Script

```bash
# Navigate to backend directory
cd backend

# Run test script
python test_db_connection.py
```

Expected output:
```
============================================================
Testing Database Connection
============================================================

Database Engine: django.db.backends.postgresql
Database Name: ai_resume_optimizer
Host: localhost
Port: 5432
User: ai_user
Connection Max Age: 600
Options: {'connect_timeout': 10, 'options': '-c statement_timeout=30000'}

Attempting to connect to database...
✓ Database connection successful!
  Query result: (1,)
  PostgreSQL version: PostgreSQL 15.1 on x86_64-pc-linux-gnu...
  Max connections: 100
  Active connections: 1

============================================================
Testing Connection Pooling Configuration
============================================================

Connection Pooling Settings:
  CONN_MAX_AGE: 600 seconds
  OPTIONS: {'connect_timeout': 10, 'options': '-c statement_timeout=30000'}

Testing multiple connections...
  ✓ Connection 1 successful
  ✓ Connection 2 successful
  ✓ Connection 3 successful

✓ Connection pooling working correctly!

============================================================
Test Summary
============================================================

Database Connection: ✓ PASSED
Connection Pooling: ✓ PASSED
Migrations: ✓ PASSED

============================================================
✓ All tests passed!
============================================================
```

### 2. Manual Connection Test

```bash
# Test connection from command line
psql -h localhost -U ai_user -d ai_resume_optimizer -c "SELECT 1;"

# Expected output:
# ?column?
# ----------
#        1
# (1 row)
```

### 3. Django Shell Test

```bash
# Navigate to backend directory
cd backend

# Open Django shell
python manage.py shell

# Test connection
>>> from django.db import connection
>>> with connection.cursor() as cursor:
...     cursor.execute("SELECT 1")
...     print(cursor.fetchone())
(1,)

# Exit shell
>>> exit()
```

---

## Troubleshooting

### Connection Refused

**Error:** `psycopg2.OperationalError: could not connect to server: Connection refused`

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   # Linux/macOS
   sudo systemctl status postgresql
   
   # Windows
   # Check Services app for PostgreSQL service
   ```

2. Verify connection parameters in `.env`:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. Check PostgreSQL is listening on the correct port:
   ```bash
   sudo netstat -tlnp | grep postgres
   ```

### Authentication Failed

**Error:** `psycopg2.OperationalError: FATAL: password authentication failed for user "ai_user"`

**Solutions:**
1. Verify password in `.env` matches database user password
2. Reset user password:
   ```bash
   psql -U postgres
   ALTER USER ai_user WITH PASSWORD 'new_password';
   \q
   ```

3. Update `.env` with new password

### Database Does Not Exist

**Error:** `psycopg2.OperationalError: FATAL: database "ai_resume_optimizer" does not exist`

**Solutions:**
1. Create database:
   ```bash
   psql -U postgres
   CREATE DATABASE ai_resume_optimizer;
   \q
   ```

2. Verify database name in `.env`

### Connection Timeout

**Error:** `psycopg2.OperationalError: could not connect to server: timeout expired`

**Solutions:**
1. Increase connection timeout in settings:
   ```python
   'OPTIONS': {
       'connect_timeout': 30,  # Increase from 10
   }
   ```

2. Check network connectivity to database host
3. Verify firewall rules allow port 5432

### Too Many Connections

**Error:** `psycopg2.OperationalError: FATAL: too many connections for role "ai_user"`

**Solutions:**
1. Increase max connections in PostgreSQL:
   ```bash
   psql -U postgres
   ALTER SYSTEM SET max_connections = 200;
   SELECT pg_reload_conf();
   \q
   ```

2. Implement connection pooling with PgBouncer
3. Reduce `CONN_MAX_AGE` to close connections faster

### Slow Queries

**Solutions:**
1. Enable query logging:
   ```bash
   psql -U postgres
   ALTER SYSTEM SET log_min_duration_statement = 1000;  # Log queries > 1 second
   SELECT pg_reload_conf();
   \q
   ```

2. Check slow query log:
   ```bash
   tail -f /var/log/postgresql/postgresql.log
   ```

3. Create indexes on frequently queried columns:
   ```bash
   psql -U ai_user -d ai_resume_optimizer
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_resumes_user_id ON resumes(user_id);
   \q
   ```

---

## Next Steps

1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Start development server: `python manage.py runserver`
4. Access admin panel: `http://localhost:8000/admin`

For more information, see:
- [Django Database Documentation](https://docs.djangoproject.com/en/4.2/ref/databases/postgresql/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/psycopg2/docs/)
