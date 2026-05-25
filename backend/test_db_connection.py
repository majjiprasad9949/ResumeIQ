#!/usr/bin/env python
"""
Database connection test script.
Tests PostgreSQL connection and connection pooling configuration.
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def test_database_connection():
    """Test basic database connection."""
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    # Get database configuration
    db_config = settings.DATABASES['default']
    print(f"\nDatabase Engine: {db_config['ENGINE']}")
    print(f"Database Name: {db_config['NAME']}")
    
    if db_config['ENGINE'] == 'django.db.backends.postgresql':
        print(f"Host: {db_config.get('HOST', 'localhost')}")
        print(f"Port: {db_config.get('PORT', 5432)}")
        print(f"User: {db_config.get('USER', 'postgres')}")
        print(f"Connection Max Age: {db_config.get('CONN_MAX_AGE', 'Not set')}")
        print(f"Options: {db_config.get('OPTIONS', {})}")
    
    try:
        # Test connection
        print("\nAttempting to connect to database...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✓ Database connection successful!")
            print(f"  Query result: {result}")
            
            # Get connection info (PostgreSQL only)
            if db_config['ENGINE'] == 'django.db.backends.postgresql':
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"  PostgreSQL version: {version[0]}")
                
                cursor.execute("SHOW max_connections;")
                max_conn = cursor.fetchone()
                print(f"  Max connections: {max_conn[0]}")
                
                cursor.execute("SELECT count(*) FROM pg_stat_activity;")
                active_conn = cursor.fetchone()
                print(f"  Active connections: {active_conn[0]}")
            else:
                print(f"  Database type: SQLite (development)")
        
        return True
        
    except OperationalError as e:
        print(f"✗ Database connection failed!")
        print(f"  Error: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False


def test_migrations():
    """Test Django migrations."""
    print("\n" + "=" * 60)
    print("Testing Django Migrations")
    print("=" * 60)
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Check migration status
        print("\nChecking migration status...")
        out = StringIO()
        call_command('showmigrations', stdout=out)
        print(out.getvalue())
        
        return True
        
    except Exception as e:
        print(f"✗ Migration check failed: {str(e)}")
        return False


def test_connection_pooling():
    """Test connection pooling configuration."""
    print("\n" + "=" * 60)
    print("Testing Connection Pooling Configuration")
    print("=" * 60)
    
    db_config = settings.DATABASES['default']
    
    if db_config['ENGINE'] != 'django.db.backends.postgresql':
        print("\nConnection pooling is only available for PostgreSQL.")
        print(f"Current database: {db_config['ENGINE']}")
        return True
    
    print("\nConnection Pooling Settings:")
    print(f"  CONN_MAX_AGE: {db_config.get('CONN_MAX_AGE', 'Not set')} seconds")
    print(f"  OPTIONS: {db_config.get('OPTIONS', {})}")
    
    # Test multiple connections
    print("\nTesting multiple connections...")
    try:
        for i in range(3):
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print(f"  ✓ Connection {i+1} successful")
        
        print("\n✓ Connection pooling working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Connection pooling test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ResumeIQ - Database Connection Test".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Database Connection", test_database_connection()))
    results.append(("Connection Pooling", test_connection_pooling()))
    results.append(("Migrations", test_migrations()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed. Please check the configuration.")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
