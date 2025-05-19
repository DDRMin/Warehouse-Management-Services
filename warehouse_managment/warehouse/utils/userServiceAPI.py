import os
import requests
from django.core.cache import cache
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Base URL for user service
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8003/api/v1")

def get_supplier_info(supplier_id):
    """
    Get supplier information from the user service with caching.
    
    Args:
        supplier_id: The ID of the supplier
        
    Returns:
        dict: Supplier information including name, or None if not found
    """
    if not supplier_id:
        return None
        
    cache_key = f"supplier_info_{supplier_id}"
    supplier_data = cache.get(cache_key)
    
    if not supplier_data:
        try:
            supplier_response = requests.get(
                f"{USER_SERVICE_URL}/suppliers/{supplier_id}/info/",
                timeout=5
            )
            
            if supplier_response.status_code == 200:
                supplier_data = supplier_response.json()
                # Cache for 1 hour
                cache.set(cache_key, supplier_data, 3600)
            else:
                logger.warning(f"Failed to fetch supplier info for ID {supplier_id}. Status: {supplier_response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error fetching supplier info for ID {supplier_id}: {str(e)}")
            return None
    
    return supplier_data

def get_supplier_name(supplier_id):
    """
    Get the formatted supplier name from user service.
    
    Args:
        supplier_id: The ID of the supplier
        
    Returns:
        str: Formatted supplier name or fallback text
    """
    supplier_data = get_supplier_info(supplier_id)
    
    if supplier_data and supplier_data.get('user'):
        user_data = supplier_data.get('user')
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        
        if first_name or last_name:
            return f"{first_name} {last_name}".strip()
    
    return f"Supplier {supplier_id}"