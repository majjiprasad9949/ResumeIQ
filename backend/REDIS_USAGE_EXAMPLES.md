# Redis Usage Examples

This document provides practical examples of how to use Redis caching in the ResumeIQ application.

## Table of Contents

1. [Basic Cache Operations](#basic-cache-operations)
2. [View-Level Caching](#view-level-caching)
3. [Query Result Caching](#query-result-caching)
4. [Cache Invalidation](#cache-invalidation)
5. [Session Management](#session-management)
6. [Celery Task Integration](#celery-task-integration)
7. [Cache Patterns](#cache-patterns)

## Basic Cache Operations

### Set and Get Values

```python
from django.core.cache import cache

# Set a value with default timeout (300 seconds)
cache.set('user_preferences_123', {'theme': 'dark', 'language': 'en'})

# Set a value with custom timeout
cache.set('resume_analysis_456', analysis_data, timeout=600)  # 10 minutes

# Get a value
preferences = cache.get('user_preferences_123')

# Get with default value if not found
preferences = cache.get('user_preferences_123', {})

# Check if key exists
if cache.has_key('user_preferences_123'):
    print("Key exists in cache")

# Delete a value
cache.delete('user_preferences_123')

# Clear all cache
cache.clear()
```

### Atomic Operations

```python
from django.core.cache import cache

# Increment a counter
cache.incr('resume_upload_count')  # Increments by 1
cache.incr('resume_upload_count', 5)  # Increments by 5

# Decrement a counter
cache.decr('resume_upload_count')  # Decrements by 1

# Get and increment
count = cache.get_or_set('analysis_count', 0)
cache.incr('analysis_count')
```

### Batch Operations

```python
from django.core.cache import cache

# Set multiple values
cache.set_many({
    'resume_1': resume_data_1,
    'resume_2': resume_data_2,
    'resume_3': resume_data_3,
}, timeout=600)

# Get multiple values
values = cache.get_many(['resume_1', 'resume_2', 'resume_3'])

# Delete multiple values
cache.delete_many(['resume_1', 'resume_2', 'resume_3'])
```

## View-Level Caching

### Cache Page Decorator

```python
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

# Cache entire view for 5 minutes
@cache_page(300)
def get_popular_keywords(request):
    keywords = extract_popular_keywords()
    return JsonResponse({'keywords': keywords})

# Cache only for GET requests
@cache_page(300)
def get_resume_list(request):
    if request.method == 'GET':
        resumes = Resume.objects.filter(user=request.user)
        return JsonResponse({'resumes': list(resumes.values())})
```

### Cache Vary Decorator

```python
from django.views.decorators.cache import cache_page, vary_on_headers

# Cache separately for different users
@cache_page(300)
@vary_on_headers('Authorization')
def get_user_dashboard(request):
    user_data = get_user_analysis_data(request.user)
    return JsonResponse(user_data)

# Cache separately for different query parameters
@cache_page(300)
@vary_on_headers('Accept-Language')
def get_localized_content(request):
    language = request.headers.get('Accept-Language', 'en')
    content = get_content_for_language(language)
    return JsonResponse(content)
```

### Manual View Caching

```python
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

class ResumeAnalysisView(APIView):
    def get(self, request, resume_id):
        # Try to get from cache
        cache_key = f'resume_analysis_{resume_id}'
        analysis = cache.get(cache_key)
        
        if analysis is None:
            # Not in cache, compute it
            analysis = perform_analysis(resume_id)
            # Store in cache for 10 minutes
            cache.set(cache_key, analysis, timeout=600)
        
        return Response(analysis)
```

## Query Result Caching

### Cache Database Queries

```python
from django.core.cache import cache
from apps.resumes.models import Resume

def get_user_resumes(user_id):
    cache_key = f'user_resumes_{user_id}'
    resumes = cache.get(cache_key)
    
    if resumes is None:
        # Query database
        resumes = list(Resume.objects.filter(
            user_id=user_id,
            is_deleted=False
        ).values('id', 'original_filename', 'created_at'))
        
        # Cache for 30 minutes
        cache.set(cache_key, resumes, timeout=1800)
    
    return resumes

def get_resume_with_analysis(resume_id):
    cache_key = f'resume_with_analysis_{resume_id}'
    data = cache.get(cache_key)
    
    if data is None:
        resume = Resume.objects.get(id=resume_id)
        analysis = AnalysisResult.objects.filter(
            resume_id=resume_id
        ).latest('created_at')
        
        data = {
            'resume': resume,
            'analysis': analysis,
        }
        
        # Cache for 1 hour
        cache.set(cache_key, data, timeout=3600)
    
    return data
```

### Cache Expensive Computations

```python
from django.core.cache import cache
from apps.analysis.services import ATSScorer

def get_ats_score_cached(resume_id, job_id):
    cache_key = f'ats_score_{resume_id}_{job_id}'
    score = cache.get(cache_key)
    
    if score is None:
        # Expensive computation
        scorer = ATSScorer()
        resume = Resume.objects.get(id=resume_id)
        job = JobDescription.objects.get(id=job_id)
        
        score = scorer.calculate_ats_score(resume, job)
        
        # Cache for 24 hours
        cache.set(cache_key, score, timeout=86400)
    
    return score
```

## Cache Invalidation

### Signal-Based Invalidation

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from apps.resumes.models import Resume

@receiver(post_save, sender=Resume)
def invalidate_resume_cache(sender, instance, created, **kwargs):
    """Invalidate cache when resume is saved"""
    # Invalidate specific resume cache
    cache.delete(f'resume_with_analysis_{instance.id}')
    
    # Invalidate user's resume list cache
    cache.delete(f'user_resumes_{instance.user_id}')
    
    # Invalidate all analysis results for this resume
    from django_redis import get_redis_connection
    redis_conn = get_redis_connection('default')
    redis_conn.delete_pattern(f'ai_resume_optimizer:ats_score_{instance.id}_*')

@receiver(post_delete, sender=Resume)
def invalidate_resume_on_delete(sender, instance, **kwargs):
    """Invalidate cache when resume is deleted"""
    cache.delete(f'resume_with_analysis_{instance.id}')
    cache.delete(f'user_resumes_{instance.user_id}')
```

### Manual Invalidation

```python
from django.core.cache import cache
from django_redis import get_redis_connection

def update_resume_and_invalidate(resume_id, new_data):
    """Update resume and invalidate related caches"""
    resume = Resume.objects.get(id=resume_id)
    
    # Update resume
    for key, value in new_data.items():
        setattr(resume, key, value)
    resume.save()
    
    # Invalidate caches
    cache.delete(f'resume_with_analysis_{resume_id}')
    cache.delete(f'user_resumes_{resume.user_id}')
    
    # Invalidate all analysis results
    redis_conn = get_redis_connection('default')
    redis_conn.delete_pattern(f'ai_resume_optimizer:ats_score_{resume_id}_*')

def clear_user_cache(user_id):
    """Clear all cache for a specific user"""
    redis_conn = get_redis_connection('default')
    
    # Delete user-specific keys
    redis_conn.delete_pattern(f'ai_resume_optimizer:user_resumes_{user_id}')
    redis_conn.delete_pattern(f'ai_resume_optimizer:resume_analysis_*')
    redis_conn.delete_pattern(f'ai_resume_optimizer:ats_score_*')
```

## Session Management

### Store User Data in Session

```python
from django.contrib.auth.decorators import login_required

@login_required
def set_user_preferences(request):
    """Store user preferences in session"""
    preferences = {
        'theme': request.POST.get('theme', 'light'),
        'language': request.POST.get('language', 'en'),
        'notifications': request.POST.get('notifications', True),
    }
    
    request.session['user_preferences'] = preferences
    request.session.modified = True
    
    return JsonResponse({'status': 'preferences saved'})

@login_required
def get_user_preferences(request):
    """Retrieve user preferences from session"""
    preferences = request.session.get('user_preferences', {
        'theme': 'light',
        'language': 'en',
        'notifications': True,
    })
    
    return JsonResponse(preferences)
```

### Session Expiration

```python
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def check_session_expiration(request):
    """Check session expiration time"""
    session_age = settings.SESSION_COOKIE_AGE  # 86400 seconds (24 hours)
    session_created = request.session.get_expiry_age()
    
    return JsonResponse({
        'session_age': session_age,
        'session_created': session_created,
        'expires_in': session_age - session_created,
    })
```

## Celery Task Integration

### Cache Task Results

```python
from celery import shared_task
from django.core.cache import cache
from apps.analysis.services import ATSScorer

@shared_task
def calculate_ats_score_async(resume_id, job_id):
    """Calculate ATS score asynchronously and cache result"""
    cache_key = f'ats_score_{resume_id}_{job_id}'
    
    # Check if already cached
    score = cache.get(cache_key)
    if score is not None:
        return score
    
    # Calculate score
    scorer = ATSScorer()
    resume = Resume.objects.get(id=resume_id)
    job = JobDescription.objects.get(id=job_id)
    
    score = scorer.calculate_ats_score(resume, job)
    
    # Cache result for 24 hours
    cache.set(cache_key, score, timeout=86400)
    
    return score

@shared_task
def invalidate_analysis_cache(resume_id):
    """Invalidate analysis cache for a resume"""
    from django_redis import get_redis_connection
    redis_conn = get_redis_connection('default')
    
    # Delete all analysis results for this resume
    redis_conn.delete_pattern(f'ai_resume_optimizer:ats_score_{resume_id}_*')
    redis_conn.delete_pattern(f'ai_resume_optimizer:resume_analysis_{resume_id}')
```

### Delayed Task Execution

```python
from celery import shared_task
from django.core.cache import cache
import time

@shared_task
def process_resume_with_cache(resume_id):
    """Process resume and cache intermediate results"""
    cache_key = f'resume_processing_{resume_id}'
    
    # Mark as processing
    cache.set(cache_key, {'status': 'processing'}, timeout=3600)
    
    try:
        # Step 1: Parse resume
        cache.set(cache_key, {'status': 'parsing'}, timeout=3600)
        parsed_data = parse_resume(resume_id)
        
        # Step 2: Extract keywords
        cache.set(cache_key, {'status': 'extracting_keywords'}, timeout=3600)
        keywords = extract_keywords(parsed_data)
        
        # Step 3: Analyze semantics
        cache.set(cache_key, {'status': 'analyzing_semantics'}, timeout=3600)
        semantic_data = analyze_semantics(parsed_data)
        
        # Mark as complete
        result = {
            'status': 'complete',
            'parsed_data': parsed_data,
            'keywords': keywords,
            'semantic_data': semantic_data,
        }
        cache.set(cache_key, result, timeout=86400)
        
        return result
        
    except Exception as e:
        cache.set(cache_key, {'status': 'error', 'error': str(e)}, timeout=3600)
        raise
```

## Cache Patterns

### Cache-Aside Pattern

```python
from django.core.cache import cache

def get_data_cache_aside(key, fetch_function, timeout=300):
    """
    Cache-aside pattern: Check cache first, fetch if not found
    
    Args:
        key: Cache key
        fetch_function: Function to call if cache miss
        timeout: Cache timeout in seconds
    
    Returns:
        Cached or fetched data
    """
    data = cache.get(key)
    
    if data is None:
        data = fetch_function()
        cache.set(key, data, timeout=timeout)
    
    return data

# Usage
def get_resume_data(resume_id):
    return get_data_cache_aside(
        f'resume_{resume_id}',
        lambda: Resume.objects.get(id=resume_id),
        timeout=600
    )
```

### Write-Through Pattern

```python
from django.core.cache import cache

def update_data_write_through(key, data, save_function, timeout=300):
    """
    Write-through pattern: Update cache and database together
    
    Args:
        key: Cache key
        data: Data to update
        save_function: Function to save to database
        timeout: Cache timeout in seconds
    """
    # Update database first
    save_function(data)
    
    # Update cache
    cache.set(key, data, timeout=timeout)

# Usage
def update_resume(resume_id, new_data):
    update_data_write_through(
        f'resume_{resume_id}',
        new_data,
        lambda data: Resume.objects.filter(id=resume_id).update(**data),
        timeout=600
    )
```

### Write-Behind Pattern

```python
from django.core.cache import cache
from celery import shared_task

def update_data_write_behind(key, data, save_task, timeout=300):
    """
    Write-behind pattern: Update cache immediately, save to database asynchronously
    
    Args:
        key: Cache key
        data: Data to update
        save_task: Celery task to save to database
        timeout: Cache timeout in seconds
    """
    # Update cache immediately
    cache.set(key, data, timeout=timeout)
    
    # Schedule database update asynchronously
    save_task.delay(key, data)

@shared_task
def save_resume_to_db(resume_id, data):
    """Celery task to save resume to database"""
    Resume.objects.filter(id=resume_id).update(**data)

# Usage
def update_resume_async(resume_id, new_data):
    update_data_write_behind(
        f'resume_{resume_id}',
        new_data,
        save_resume_to_db,
        timeout=600
    )
```

### Stampede Prevention

```python
from django.core.cache import cache
import time

def get_data_with_stampede_prevention(key, fetch_function, timeout=300):
    """
    Prevent cache stampede by using a lock
    
    Args:
        key: Cache key
        fetch_function: Function to call if cache miss
        timeout: Cache timeout in seconds
    """
    data = cache.get(key)
    
    if data is None:
        lock_key = f'{key}:lock'
        
        # Try to acquire lock
        if cache.add(lock_key, True, timeout=10):
            try:
                # Double-check cache
                data = cache.get(key)
                if data is None:
                    data = fetch_function()
                    cache.set(key, data, timeout=timeout)
            finally:
                cache.delete(lock_key)
        else:
            # Wait for lock to be released
            for _ in range(10):
                time.sleep(0.1)
                data = cache.get(key)
                if data is not None:
                    break
    
    return data
```

## Best Practices

1. **Use Meaningful Cache Keys**: Include resource type and ID
   ```python
   cache_key = f'resume_analysis_{resume_id}_{job_id}'
   ```

2. **Set Appropriate Timeouts**: Balance between freshness and performance
   ```python
   # Short-lived: 5 minutes
   cache.set(key, data, timeout=300)
   
   # Medium-lived: 1 hour
   cache.set(key, data, timeout=3600)
   
   # Long-lived: 24 hours
   cache.set(key, data, timeout=86400)
   ```

3. **Handle Cache Misses Gracefully**: Always have a fallback
   ```python
   data = cache.get(key)
   if data is None:
       data = fetch_from_database()
   ```

4. **Invalidate Strategically**: Don't over-invalidate
   ```python
   # Good: Invalidate specific keys
   cache.delete(f'resume_{resume_id}')
   
   # Bad: Clear entire cache
   cache.clear()
   ```

5. **Monitor Cache Performance**: Track hit/miss rates
   ```python
   from django_redis import get_redis_connection
   redis_conn = get_redis_connection('default')
   info = redis_conn.info()
   hit_rate = info['keyspace_hits'] / (info['keyspace_hits'] + info['keyspace_misses'])
   ```

## References

- [Django Cache Framework](https://docs.djangoproject.com/en/4.2/topics/cache/)
- [django-redis Documentation](https://github.com/jazzband/django-redis)
- [Redis Commands](https://redis.io/commands/)
- [Caching Patterns](https://en.wikipedia.org/wiki/Cache_(computing)#Policies)
