# Redis Quick Start Guide

## 5-Minute Setup

### 1. Start Redis

```bash
# Using Docker (easiest)
docker run -d -p 6379:6379 redis:latest

# Or using Homebrew (macOS)
brew install redis && brew services start redis

# Or using apt (Linux)
sudo apt-get install redis-server && sudo systemctl start redis-server
```

### 2. Verify Redis is Running

```bash
redis-cli ping
# Should return: PONG
```

### 3. Install Python Packages

```bash
cd backend
pip install -r requirements.txt
```

### 4. Test Configuration

```bash
python manage.py shell < test_redis_connection.py
```

---

## Common Commands

### Cache Operations

```python
from django.core.cache import cache

# Set value
cache.set('key', 'value', timeout=300)

# Get value
value = cache.get('key')

# Delete value
cache.delete('key')

# Clear all
cache.clear()
```

### Redis CLI

```bash
redis-cli ping              # Test connection
redis-cli DBSIZE            # Show number of keys
redis-cli KEYS "*"          # List all keys
redis-cli FLUSHDB           # Clear database
redis-cli INFO              # Server info
redis-cli MONITOR           # Monitor commands
```

---

## Environment Variables

Add to `.env`:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Start Redis: `redis-server` |
| Timeout errors | Increase timeout in settings.py |
| Memory full | Configure `maxmemory-policy` in Redis |
| Slow performance | Check connection pool size |

---

## Documentation

- **Full Setup**: See `REDIS_SETUP.md`
- **Usage Examples**: See `REDIS_USAGE_EXAMPLES.md`
- **Implementation Details**: See `REDIS_IMPLEMENTATION_SUMMARY.md`

---

## Next Steps

1. ✅ Redis installed and running
2. ✅ Python packages installed
3. ✅ Configuration verified
4. Start using cache in your views:

```python
from django.core.cache import cache

def my_view(request):
    data = cache.get('my_key')
    if data is None:
        data = expensive_operation()
        cache.set('my_key', data, timeout=300)
    return JsonResponse(data)
```

---

## Support

For detailed information, see the documentation files in the backend directory.
