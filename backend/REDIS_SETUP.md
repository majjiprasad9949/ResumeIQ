# Redis Configuration Guide

## Overview

Redis is configured in the ResumeIQ application for:
1. **Query Caching**: Cache frequently accessed data to reduce database load
2. **Session Storage**: Store user sessions in Redis for distributed systems
3. **Celery Broker**: Message broker for asynchronous task processing
4. **Result Backend**: Store results of asynchronous tasks

## Installation

### Prerequisites
- Redis server installed and running
- Python packages: `redis==5.0.1` and `django-redis==5.4.0`

### Install Redis

#### On Windows (using WSL or Docker)
```bash
# Using Docker (recommended)
docker run -d -p 6379:6379 redis:latest

# Or using WSL with Ubuntu
wsl
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
```

#### On macOS
```bash
# Using Homebrew
brew install redis
brew services start redis
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Verify Redis Installation
```bash
redis-cli ping
# Should return: PONG
```

## Configuration

### Environment Variables

Configure Redis connection in your `.env` file:

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Leave empty if no password, or set your password

# Optional: Override Celery URLs if different from main Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Django Settings

The following Redis configuration is automatically applied in `config/settings.py`:

#### Cache Backend Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,  # Gracefully handle Redis failures
        },
        'KEY_PREFIX': 'ai_resume_optimizer',
        'TIMEOUT': 300,  # 5 minutes default timeout
    }
}
```

#### Session Storage Configuration
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

#### Celery Configuration
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
```

## Connection Pooling

Redis connection pooling is configured with the following parameters:

- **max_connections**: 50 - Maximum number of connections in the pool
- **retry_on_timeout**: True - Retry connection on timeout
- **SOCKET_CONNECT_TIMEOUT**: 5 seconds - Connection timeout
- **SOCKET_TIMEOUT**: 5 seconds - Socket timeout
- **COMPRESSOR**: zlib - Compress cached values to save memory

## Cache Usage

### Using Django Cache Framework

```python
from django.core.cache import cache

# Set a value
cache.set('resume_analysis_123', analysis_data, timeout=300)

# Get a value
analysis_data = cache.get('resume_analysis_123')

# Delete a value
cache.delete('resume_analysis_123')

# Clear all cache
cache.clear()
```

### Cache Decorator

```python
from django.views.decorators.cache import cache_page

@cache_page(300)  # Cache for 5 minutes
def get_resume_analysis(request, resume_id):
    # View logic here
    pass
```

### Cache Invalidation

```python
from django.core.cache import cache

# Invalidate specific cache keys
cache.delete('resume_analysis_123')
cache.delete('job_description_456')

# Invalidate pattern (requires redis-py)
from django_redis import get_redis_connection
redis_conn = get_redis_connection('default')
redis_conn.delete_pattern('ai_resume_optimizer:resume_*')
```

## Session Management

Sessions are automatically stored in Redis when configured. No additional code is needed.

### Session Usage

```python
# Store data in session
request.session['user_preferences'] = {'theme': 'dark'}

# Retrieve data from session
preferences = request.session.get('user_preferences')

# Delete session data
del request.session['user_preferences']
```

## Monitoring and Debugging

### Check Redis Connection

```bash
redis-cli
> PING
PONG

> INFO
# Shows Redis server information

> DBSIZE
# Shows number of keys in current database

> KEYS *
# Lists all keys (use with caution in production)

> KEYS ai_resume_optimizer:*
# Lists all keys with our prefix
```

### Monitor Cache Usage

```python
from django_redis import get_redis_connection

redis_conn = get_redis_connection('default')
info = redis_conn.info()

print(f"Used Memory: {info['used_memory_human']}")
print(f"Connected Clients: {info['connected_clients']}")
print(f"Total Commands: {info['total_commands_processed']}")
```

### Clear Cache in Django Shell

```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.clear()
print("Cache cleared successfully")
```

## Production Deployment

### Redis Persistence

For production, enable Redis persistence:

#### RDB (Snapshot) Persistence
```bash
# In redis.conf
save 900 1      # Save if 1 key changed in 900 seconds
save 300 10     # Save if 10 keys changed in 300 seconds
save 60 10000   # Save if 10000 keys changed in 60 seconds
```

#### AOF (Append-Only File) Persistence
```bash
# In redis.conf
appendonly yes
appendfsync everysec
```

### Redis Replication

For high availability, set up Redis replication:

```bash
# On replica server, in redis.conf
replicaof master_host master_port
```

### Redis Cluster

For large-scale deployments, use Redis Cluster:

```python
# Update settings.py for cluster
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            'redis://node1:6379/0',
            'redis://node2:6379/0',
            'redis://node3:6379/0',
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.ShardClient',
        }
    }
}
```

### AWS ElastiCache

For AWS deployments, use ElastiCache:

```env
REDIS_HOST=your-elasticache-endpoint.ng.0001.use1.cache.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=your-auth-token
```

## Troubleshooting

### Connection Refused
```
Error: ConnectionRefusedError: [Errno 111] Connection refused
```
**Solution**: Ensure Redis server is running
```bash
redis-cli ping
# If not running, start Redis
redis-server
```

### Timeout Errors
```
Error: redis.exceptions.TimeoutError
```
**Solution**: Increase timeout values in settings.py
```python
'SOCKET_CONNECT_TIMEOUT': 10,
'SOCKET_TIMEOUT': 10,
```

### Memory Issues
```
Error: OOM command not allowed when used memory > 'maxmemory'
```
**Solution**: Configure Redis memory policy
```bash
# In redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Authentication Failed
```
Error: WRONGPASS invalid username-password pair
```
**Solution**: Verify Redis password in .env file
```env
REDIS_PASSWORD=your-correct-password
```

## Performance Optimization

### Cache Key Naming Convention

Use consistent naming for cache keys:
```python
# Format: app:resource:id:version
cache_key = f'ai_resume_optimizer:resume_analysis:{resume_id}:v1'
```

### Cache Warming

Pre-populate cache with frequently accessed data:
```python
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Warm up cache with frequently accessed data
        cache.set('popular_keywords', get_popular_keywords(), timeout=3600)
        self.stdout.write('Cache warmed successfully')
```

### Cache Invalidation Strategy

Implement smart cache invalidation:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

@receiver(post_save, sender=Resume)
def invalidate_resume_cache(sender, instance, **kwargs):
    cache.delete(f'resume_analysis_{instance.id}')
    cache.delete(f'resume_versions_{instance.id}')
```

## Testing

### Test Redis Connection

Run the provided test script:
```bash
python manage.py shell < test_redis_connection.py
```

Or manually in Django shell:
```bash
python manage.py shell
```

```python
from django.core.cache import cache

# Test set and get
cache.set('test_key', 'test_value', timeout=60)
value = cache.get('test_key')
print(f"Cache test: {value}")

# Test session
from django.contrib.sessions.models import Session
print(f"Sessions in database: {Session.objects.count()}")
```

## References

- [Django Cache Framework](https://docs.djangoproject.com/en/4.2/topics/cache/)
- [django-redis Documentation](https://github.com/jazzband/django-redis)
- [Redis Documentation](https://redis.io/documentation)
- [Redis CLI Commands](https://redis.io/commands/)
- [Celery with Redis](https://docs.celeryproject.io/en/stable/getting-started/brokers/redis.html)

## Summary

Redis is now configured for:
- ✅ Query caching with 5-minute default timeout
- ✅ Session storage with 24-hour expiration
- ✅ Connection pooling with 50 max connections
- ✅ Celery task broker and result backend
- ✅ Automatic compression of cached values
- ✅ Graceful failure handling

The configuration is production-ready and can be easily scaled for high-traffic deployments.
