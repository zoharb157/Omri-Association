#!/usr/bin/env python3
"""
Cache Manager for Omri Association Dashboard
Provides intelligent caching for data and computations
"""

import streamlit as st
import pandas as pd
import time
import hashlib
import pickle
from typing import Any, Optional, Dict
from functools import wraps
from config import get_setting

class CacheManager:
    """Manages caching for dashboard data and computations"""
    
    def __init__(self):
        self.cache_ttl = get_setting('CACHE_TTL', 300)  # 5 minutes default
        self.max_cache_size = 100  # Maximum number of cached items
    
    def _generate_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate a unique cache key for function call"""
        # Create a string representation of arguments
        args_str = str(args) + str(sorted(kwargs.items()))
        # Hash the string to create a shorter key
        return f"{func_name}_{hashlib.md5(args_str.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        if not get_setting('ENABLE_CACHING', True):
            return None
        
        if key in st.session_state:
            cached_item = st.session_state[key]
            if isinstance(cached_item, dict) and 'expires_at' in cached_item:
                if time.time() < cached_item['expires_at']:
                    return cached_item['data']
                else:
                    # Cache expired, remove it
                    del st.session_state[key]
        
        return None
    
    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Set item in cache with TTL"""
        if not get_setting('ENABLE_CACHING', True):
            return
        
        # Clean up old cache entries if we're at capacity
        self._cleanup_cache()
        
        ttl = ttl or self.cache_ttl
        expires_at = time.time() + ttl
        
        st.session_state[key] = {
            'data': data,
            'expires_at': expires_at,
            'created_at': time.time()
        }
    
    def invalidate(self, key: str) -> None:
        """Invalidate a specific cache entry"""
        if key in st.session_state:
            del st.session_state[key]
    
    def clear_all(self) -> None:
        """Clear all cache entries"""
        keys_to_remove = []
        for key in st.session_state.keys():
            if key.startswith('cache_'):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    def _cleanup_cache(self) -> None:
        """Remove expired cache entries and old entries if at capacity"""
        current_time = time.time()
        keys_to_remove = []
        cache_entries = []
        
        # Find all cache entries
        for key in st.session_state.keys():
            if key.startswith('cache_'):
                cached_item = st.session_state[key]
                if isinstance(cached_item, dict) and 'expires_at' in cached_item:
                    if current_time >= cached_item['expires_at']:
                        keys_to_remove.append(key)
                    else:
                        cache_entries.append((key, cached_item['created_at']))
        
        # Remove expired entries
        for key in keys_to_remove:
            del st.session_state[key]
        
        # If still at capacity, remove oldest entries
        if len(cache_entries) >= self.max_cache_size:
            # Sort by creation time and remove oldest
            cache_entries.sort(key=lambda x: x[1])
            keys_to_remove = [key for key, _ in cache_entries[:-self.max_cache_size]]
            for key in keys_to_remove:
                del st.session_state[key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_count = 0
        expired_count = 0
        total_size = 0
        
        current_time = time.time()
        
        for key in st.session_state.keys():
            if key.startswith('cache_'):
                cached_item = st.session_state[key]
                if isinstance(cached_item, dict) and 'expires_at' in cached_item:
                    cache_count += 1
                    if current_time >= cached_item['expires_at']:
                        expired_count += 1
                    
                    # Estimate size (rough calculation)
                    try:
                        item_size = len(pickle.dumps(cached_item['data']))
                        total_size += item_size
                    except:
                        pass
        
        return {
            'total_entries': cache_count,
            'expired_entries': expired_count,
            'active_entries': cache_count - expired_count,
            'estimated_size_mb': round(total_size / (1024 * 1024), 2),
            'max_cache_size': self.max_cache_size,
            'cache_ttl': self.cache_ttl
        }

# Global cache manager instance
cache_manager = CacheManager()

def cached(ttl: Optional[int] = None):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"cache_{cache_manager._generate_cache_key(func.__name__, *args, **kwargs)}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    return cache_manager

def clear_cache():
    """Clear all cache entries"""
    cache_manager.clear_all()

def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    return cache_manager.get_cache_stats()

# Cache-specific functions for common data types
def cache_dataframe(key: str, df: pd.DataFrame, ttl: Optional[int] = None) -> None:
    """Cache a pandas DataFrame"""
    cache_manager.set(f"cache_df_{key}", df, ttl)

def get_cached_dataframe(key: str) -> Optional[pd.DataFrame]:
    """Get a cached pandas DataFrame"""
    return cache_manager.get(f"cache_df_{key}")

def cache_dict(key: str, data: Dict, ttl: Optional[int] = None) -> None:
    """Cache a dictionary"""
    cache_manager.set(f"cache_dict_{key}", data, ttl)

def get_cached_dict(key: str) -> Optional[Dict]:
    """Get a cached dictionary"""
    return cache_manager.get(f"cache_dict_{key}")

def cache_numeric(key: str, value: float, ttl: Optional[int] = None) -> None:
    """Cache a numeric value"""
    cache_manager.set(f"cache_num_{key}", value, ttl)

def get_cached_numeric(key: str) -> Optional[float]:
    """Get a cached numeric value"""
    return cache_manager.get(f"cache_num_{key}")

# Streamlit-specific cache functions
def st_cache_data(key: str, data: Any, ttl: Optional[int] = None) -> None:
    """Cache data using Streamlit's session state"""
    if not get_setting('ENABLE_CACHING', True):
        return
    
    expires_at = time.time() + (ttl or cache_manager.cache_ttl)
    st.session_state[f"st_cache_{key}"] = {
        'data': data,
        'expires_at': expires_at
    }

def st_get_cached_data(key: str) -> Optional[Any]:
    """Get cached data from Streamlit's session state"""
    if not get_setting('ENABLE_CACHING', True):
        return None
    
    cache_key = f"st_cache_{key}"
    if cache_key in st.session_state:
        cached_item = st.session_state[cache_key]
        if time.time() < cached_item['expires_at']:
            return cached_item['data']
        else:
            # Cache expired, remove it
            del st.session_state[cache_key]
    
    return None
