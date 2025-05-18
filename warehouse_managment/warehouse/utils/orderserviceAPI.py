import requests
import httpx
from rest_framework import status
from rest_framework.response import Response

# Base URLs
ORDER_SERVICE_URL = "http://blocktrack-backend:8000/api/v0/orders"
SUPPLIER_REQUEST_URL = "http://blocktrack-backend:8000/api/v0/supplier-request"

# Order status update
def update_order_status(order_id, status_payload):
    """
    Update the status of an order in the order service.
    
    Args:
        order_id: The ID of the order to update
        status_payload: JSON payload with status information
        
    Returns:
        response: The response from the order service
        
    Raises:
        requests.RequestException: If the request fails
    """
    print(f"Updating order status for order ID: {order_id}")
    response = requests.patch(
        f"{ORDER_SERVICE_URL}/{order_id}/status/",
        json=status_payload,
        timeout=120
    )
    response.raise_for_status()
    return response

# Supplier request update
def update_supplier_request(request_id, status_update_payload):
    """
    Update a supplier request in the supplier service.
    
    Args:
        request_id: The ID of the supplier request to update
        status_update_payload: JSON payload with status information
        
    Returns:
        response: The response from the supplier service
        
    Raises:
        requests.RequestException: If the request fails
    """
    response = requests.patch(
        f"{SUPPLIER_REQUEST_URL}/request/{request_id}/",
        json=status_update_payload,
        timeout=120
    )
    response.raise_for_status()
    return response

# Get orders for a warehouse
def get_warehouse_orders(warehouse_id):
    """
    Get all orders for a specific warehouse.
    
    Args:
        warehouse_id: The ID of the warehouse
        
    Returns:
        dict: The orders data
        
    Raises:
        httpx.RequestError: If there's a network error
        httpx.HTTPStatusError: If the request fails with a 4xx/5xx status
    """
    url = f"{ORDER_SERVICE_URL}/warehouse/{warehouse_id}?minimal=True&status=pending"
    response = httpx.get(url, timeout=120)
    response.raise_for_status()
    return response.json()
