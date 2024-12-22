# analytics/utils.py

import os
import ipinfo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_ip_info(ip_address):
    access_token = os.getenv('ACCESS_TOKEN')
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    
    ip_info = {
        "ip": getattr(details, 'ip', 'N/A'),
        "hostname": getattr(details, 'hostname', 'N/A'),
        "city": getattr(details, 'city', 'N/A'),
        "region": getattr(details, 'region', 'N/A'),
        "country": getattr(details, 'country', 'N/A'),
        "loc": getattr(details, 'loc', 'N/A'),
        "org": getattr(details, 'org', 'N/A'),
        "postal": getattr(details, 'postal', 'N/A'),
        "timezone": getattr(details, 'timezone', 'N/A'),
    }
    
    return ip_info