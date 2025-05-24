#!/usr/bin/env python
"""
Simple test script to verify the API endpoints.
Run this script directly from the command line:
python listing/test_api.py
"""
import os
import sys
import json
import requests

# Add the project directory to path so Django settings can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Base URL for API endpoints
BASE_URL = "http://localhost:8000/api/listing/"


def test_categories_endpoint():
    """Test the categories endpoint"""
    print("\n--- Testing Categories Endpoint ---")
    response = requests.get(f"{BASE_URL}categories/")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Retrieved {len(data['results'])} categories.")
        for category in data["results"][:3]:  # Print just first few for brevity
            print(f"- {category['name']} (slug: {category['slug']})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def test_listings_endpoint():
    """Test the listings endpoint"""
    print("\n--- Testing Listings Endpoint ---")
    response = requests.get(f"{BASE_URL}listings/")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Retrieved {len(data['results'])} listings.")
        for listing in data["results"][:3]:  # Print just first few for brevity
            print(f"- {listing['title']} (category: {listing['category_name']})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def test_filtering():
    """Test filtering capabilities"""
    print("\n--- Testing Filtering ---")
    # Exclude specific categories
    response = requests.get(f"{BASE_URL}listings/?exclude_category=sante,avocats")
    if response.status_code == 200:
        data = response.json()
        print(
            f"Success! Retrieved {len(data['results'])} listings excluding 'sante' and 'avocats'."
        )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    print("Testing Listing API endpoints...")
    print("Make sure the Django server is running on http://localhost:8000/")

    test_categories_endpoint()
    test_listings_endpoint()
    test_filtering()
