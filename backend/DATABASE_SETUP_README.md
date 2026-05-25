# Database Setup and Configuration

This document provides a comprehensive overview of the database setup for the ResumeIQ application.

## Overview

The ResumeIQ supports multiple database backends:
- **SQLite** (default for development)
- **PostgreSQL** (recommended for production)

### Current Configuration

- **Development**: SQLite (db.sqlite3)
- **Production**: PostgreSQL (recommended)

## Quick Start

### Development Setup (SQLite)

SQLite is configured by default for local development. No additional setup is required.

```bash
# Navigate to backend directory
cd backend

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Production Setup (PostgreSQL)

For production environments, PostgreSQL is recommended for better performance and scalability.

#### 1. Install PostgreSQL

See [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) for detailed installation instructions for your operating system.

#### 2. Configure Environment Variables

Update `backend/.env` or `backend/.env.production`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ai_resume_optimizer
DB_USER=ai_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

#### 3. Run Migrations

```bash
cd backend
python manage.py migrate
```

#### 4. Test Connection

```bash
python test_db_connection.py
```

## Database Configuration

### Settings.py Configuration

The database configuration in `config/settings.py` supports flexible database selection:

```python
DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3') if DB_ENGINE == 'django.db.backends.sqlite3' else config('DB_NAME', default='ai_resume_optimizer'),
        'USER': config('DB_USER', default='') if DB_ENGINE != 'django.db.backends.sqlite3' else '',
        'PASSWORD': config('DB_PASSWORD', default='') if DB_ENGINE != 'django.db.backends.sqlite3' else '',
        'HOST': config('DB_HOST', default='') if DB_ENGINE != 'django.db.backends.sqlite3' else '',
        'PORT': config('DB_PORT', default='') if DB_ENGINE != 'django.db.backends.sqlite3' else '',
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=600, cast=int),
        'OPTIONS': {
            'connect_timeout': 10,
        } if DB_ENGINE == 'django.db.backends.postgresql' else {},
    }
}

# PostgreSQL Connection Pooling Configuration
if DB_ENGINE == 'django.db.backends.postgresql':
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'options': '-c statement_timeout=30000'  # 30 second statement timeout
    }
```

### Environment Variables

The following environment variables control database configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_ENGINE` | `django.db.backends.sqlite3` | Database backend engine |
| `DB_NAME` | `db.sqlite3` | Database name or file path |
| `DB_USER` | `` | Database user (PostgreSQL only) |
| `DB_PASSWORD` | `` | Database password (PostgreSQL only) |
| `DB_HOST` | `` | Database host (PostgreSQL only) |
| `DB_PORT` | `` | Database port (PostgreSQL only) |
| `DB_CONN_MAX_AGE` | `600` | Connection pool lifetime in seconds |

## Connection Pooling

### Overview

Connection pooling improves application performance by reusing database connections instead of creating new ones for each request.

### Configuration

The application uses Django's built-in connection pooling with the following settings:

- **CONN_MAX_AGE**: 600 seconds (10 minutes)
  - Connections are reused for up to 10 minutes
  - After 10 minutes, connections are closed and new ones are created
  - This prevents stale connections and memory leaks

- **connect_timeout**: 10 seconds
  - Prevents hanging connections
  - Raises an error if connection cannot be established within 10 seconds

- **statement_timeout**: 30 seconds (30000 milliseconds)
  - Prevents long-running queries from blocking
  - Queries exceeding 30 seconds are automatically cancelled

### Performance Benefits

- **Reduced Overhead**: Eliminates connection creation/destruction overhead
- **Improved Throughput**: Allows more concurrent requests with fewer connections
- **Better Resource Utilization**: Connections are reused efficiently
- **Automatic Cleanup**: Stale connections are automatically closed

### Advanced Configuration

For high-traffic production environments, consider using PgBouncer for external connection pooling. See [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) for detailed instructions.

## Database Schema

### Core Tables

The application uses the following core tables:

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP
);
```

#### Resumes Table
```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  original_filename VARCHAR(255) NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  file_size INTEGER NOT NULL,
  file_format VARCHAR(10) NOT NULL,
  text_content TEXT NOT NULL,
  parsed_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);
```

#### Job Descriptions Table
```sql
CREATE TABLE job_descriptions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  content TEXT NOT NULL,
  parsed_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);
```

#### Analysis Results Table
```sql
CREATE TABLE analysis_results (
  id UUID PRIMARY KEY,
  resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
  job_id UUID NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
  ats_score FLOAT NOT NULL,
  score_breakdown JSONB NOT NULL,
  missing_keywords JSONB NOT NULL,
  formatting_issues JSONB NOT NULL,
  skill_gaps JSONB NOT NULL,
  recommendations JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes

The following indexes are created for performance optimization:

```sql
-- Users indexes
CREATE INDEX idx_users_email ON users(email);

-- Resumes indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at);

-- Job Descriptions indexes
CREATE INDEX idx_job_descriptions_user_id ON job_descriptions(user_id);
CREATE INDEX idx_job_descriptions_created_at ON job_descriptions(created_at);

-- Analysis Results indexes
CREATE INDEX idx_analysis_results_resume_id ON analysis_results(resume_id);
CREATE INDEX idx_analysis_results_job_id ON analysis_results(job_id);
```

## Migrations

### Running Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate users

# Show migration status
python manage.py showmigrations

# Reverse migrations
python manage.py migrate users 0001
```

### Creating Migrations

```bash
# Create new migration after model changes
python manage.py makemigrations

# Create migration with custom name
python manage.py makemigrations users --name add_user_fields
```

## Testing Database Connection

### Automated Test

Run the provided test script to verify database configuration:

```bash
python test_db_connection.py
```

Expected output:
```
✓ Database Connection: PASSED
✓ Connection Pooling: PASSED
✓ Migrations: PASSED
```

### Manual Test

Test connection from Django shell:

```bash
python manage.py shell

>>> from django.db import connection
>>> with connection.cursor() as cursor:
...     cursor.execute("SELECT 1")
...     print(cursor.fetchone())
(1,)

>>> exit()
```

### Command Line Test

Test connection using psql (PostgreSQL only):

```bash
psql -h localhost -U ai_user -d ai_resume_optimizer -c "SELECT 1;"
```

## Troubleshooting

### Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
1. Verify PostgreSQL is running
2. Check connection parameters in `.env`
3. Verify firewall allows port 5432

See [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) for detailed troubleshooting.

### Migration Issues

**Problem**: `django.db.utils.ProgrammingError: relation "users_customuser" does not exist`

**Solutions**:
1. Run migrations: `python manage.py migrate`
2. Check migration status: `python manage.py showmigrations`
3. Reset database (development only): `python manage.py flush`

### Performance Issues

**Problem**: Slow queries or high database load

**Solutions**:
1. Enable query logging to identify slow queries
2. Create indexes on frequently queried columns
3. Implement connection pooling with PgBouncer
4. Optimize queries using Django ORM

## Best Practices

### Development

- Use SQLite for local development
- Keep `.env` file with development settings
- Run migrations after pulling code changes
- Use `python manage.py shell` for database exploration

### Production

- Use PostgreSQL for production
- Use `.env.production` for production settings
- Enable SSL/TLS for database connections
- Implement automated backups
- Monitor database performance
- Use connection pooling (PgBouncer)
- Enable query logging for debugging

### Security

- Use strong passwords for database users
- Restrict database access to application servers
- Use environment variables for sensitive data
- Enable SSL/TLS for remote connections
- Regularly update PostgreSQL
- Implement database-level access controls

## References

- [Django Database Documentation](https://docs.djangoproject.com/en/4.2/ref/databases/postgresql/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/psycopg2/docs/)
- [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) - Detailed PostgreSQL setup guide

## Support

For issues or questions:
1. Check [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) for PostgreSQL-specific help
2. Review Django documentation
3. Check application logs for error messages
4. Run `python test_db_connection.py` to diagnose issues
