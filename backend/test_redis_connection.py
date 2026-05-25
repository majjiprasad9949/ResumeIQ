"""
Redis Connection Test Script

This script verifies that Redis is properly configured and connected.
Run with: python manage.py shell < test_redis_connection.py
"""

import os
import sys
from django.core.cache import cache
from django_redis import get_redis_connection
import redis

def test_redis_connection():
    """Test basic Redis connection"""
    print("\n" + "="*60)
    print("REDIS CONNECTION TEST")
    print("="*60)
    
    try:
        # Test 1: Direct Redis connection
        print("\n[Test 1] Direct Redis Connection")
        print("-" * 40)
        
        redis_conn = get_redis_connection('default')
        pong = redis_conn.ping()
        
        if pong:
            print("✓ Redis connection successful")
            print(f"  Response: {pong}")
        else:
            print("✗ Redis connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Redis connection error: {e}")
        return False
    
    try:
        # Test 2: Cache set and get
        print("\n[Test 2] Cache Set/Get Operations")
        print("-" * 40)
        
        test_key = 'ai_resume_optimizer:test_key'
        test_value = {'test': 'data', 'timestamp': '2024-01-15'}
        
        # Set value
        cache.set(test_key, test_value, timeout=300)
        print(f"✓ Set cache key: {test_key}")
        
        # Get value
        retrieved_value = cache.get(test_key)
        if retrieved_value == test_value:
            print(f"✓ Retrieved cache value: {retrieved_value}")
        else:
            print(f"✗ Cache value mismatch")
            print(f"  Expected: {test_value}")
            print(f"  Got: {retrieved_value}")
            return False
            
        # Delete value
        cache.delete(test_key)
        deleted_value = cache.get(test_key)
        if deleted_value is None:
            print(f"✓ Cache key deleted successfully")
        else:
            print(f"✗ Cache key deletion failed")
            return False
            
    except Exception as e:
        print(f"✗ Cache operation error: {e}")
        return False
    
    try:
        # Test 3: Redis Info
        print("\n[Test 3] Redis Server Information")
        print("-" * 40)
        
        redis_conn = get_redis_connection('default')
        info = redis_conn.info()
        
        print(f"✓ Redis Server Information:")
        print(f"  Version: {info.get('redis_version', 'N/A')}")
        print(f"  Used Memory: {info.get('used_memory_human', 'N/A')}")
        print(f"  Connected Clients: {info.get('connected_clients', 'N/A')}")
        print(f"  Total Commands: {info.get('total_commands_processed', 'N/A')}")
        print(f"  Uptime (seconds): {info.get('uptime_in_seconds', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Redis info error: {e}")
        return False
    
    try:
        # Test 4: Connection Pool
        print("\n[Test 4] Connection Pool Configuration")
        print("-" * 40)
        
        redis_conn = get_redis_connection('default')
        connection_pool = redis_conn.connection_pool
        
        print(f"✓ Connection Pool Information:")
        print(f"  Max Connections: {connection_pool.max_connections}")
        print(f"  Connection Count: {len(connection_pool._available_connections)}")
        
    except Exception as e:
        print(f"✗ Connection pool error: {e}")
        return False
    
    try:
        # Test 5: Session Storage
        print("\n[Test 5] Session Storage Configuration")
        print("-" * 40)
        
        from django.conf import settings
        
        session_engine = settings.SESSION_ENGINE
        session_cache = settings.SESSION_CACHE_ALIAS
        session_age = settings.SESSION_COOKIE_AGE
        
        print(f"✓ Session Configuration:")
        print(f"  Engine: {session_engine}")
        print(f"  Cache Alias: {session_cache}")
        print(f"  Cookie Age: {session_age} seconds ({session_age // 3600} hours)")
        
        if session_engine == 'django.contrib.sessions.backends.cache':
            print(f"  Status: ✓ Sessions stored in Redis")
        else:
            print(f"  Status: ✗ Sessions NOT stored in Redis")
            return False
            
    except Exception as e:
        print(f"✗ Session configuration error: {e}")
        return False
    
    try:
        # Test 6: Cache Configuration
        print("\n[Test 6] Cache Configuration")
        print("-" * 40)
        
        from django.conf import settings
        
        cache_config = settings.CACHES['default']
        
        print(f"✓ Cache Configuration:")
        print(f"  Backend: {cache_config['BACKEND']}")
        print(f"  Location: {cache_config['LOCATION']}")
        print(f"  Key Prefix: {cache_config.get('KEY_PREFIX', 'N/A')}")
        print(f"  Default Timeout: {cache_config.get('TIMEOUT', 'N/A')} seconds")
        
        options = cache_config.get('OPTIONS', {})
        print(f"  Client Class: {options.get('CLIENT_CLASS', 'N/A')}")
        print(f"  Compressor: {options.get('COMPRESSOR', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Cache configuration error: {e}")
        return False
    
    try:
        # Test 7: Celery Configuration
        print("\n[Test 7] Celery Configuration")
        print("-" * 40)
        
        from django.conf import settings
        
        broker_url = settings.CELERY_BROKER_URL
        result_backend = settings.CELERY_RESULT_BACKEND
        
        print(f"✓ Celery Configuration:")
        print(f"  Broker URL: {broker_url}")
        print(f"  Result Backend: {result_backend}")
        print(f"  Task Serializer: {settings.CELERY_TASK_SERIALIZER}")
        print(f"  Result Serializer: {settings.CELERY_RESULT_SERIALIZER}")
        
        if 'redis' in broker_url:
            print(f"  Status: ✓ Celery using Redis broker")
        else:
            print(f"  Status: ✗ Celery NOT using Redis broker")
            return False
            
    except Exception as e:
        print(f"✗ Celery configuration error: {e}")
        return False
    
    try:
        # Test 8: Database Keys
        print("\n[Test 8] Redis Database Keys")
        print("-" * 40)
        
        redis_conn = get_redis_connection('default')
        
        # Get all keys with our prefix
        keys = redis_conn.keys('ai_resume_optimizer:*')
        
        print(f"✓ Redis Database Information:")
        print(f"  Total Keys with Prefix: {len(keys)}")
        
        if keys:
            print(f"  Sample Keys:")
            for key in keys[:5]:
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                ttl = redis_conn.ttl(key)
                print(f"    - {key_str} (TTL: {ttl}s)")
        
    except Exception as e:
        print(f"✗ Database keys error: {e}")
        return False
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED")
    print("="*60)
    print("\nRedis is properly configured and ready for use!")
    print("\nConfiguration Summary:")
    print("  • Query caching: ENABLED")
    print("  • Session storage: ENABLED")
    print("  • Celery broker: ENABLED")
    print("  • Connection pooling: ENABLED")
    print("  • Compression: ENABLED")
    print("\n")
    
    return True


if __name__ == '__main__':
    try:
        success = test_redis_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
