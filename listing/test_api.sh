#!/bin/zsh

# Change to project directory
cd /Users/awf/Projects/software-development/dev/clients/django-react-pamoja/pamoja-nfn.com

# Activate virtual environment
source _venv/bin/activate

echo "\n===== Testing Listing API =====\n"
echo "Make sure you're running the Django server with: python manage.py runserver\n"

# Test Categories endpoint
echo "\n----- Testing Categories Endpoint -----\n"
curl -s http://localhost:8000/api/listing/categories/ | python -m json.tool | head -20

# Test Listings endpoint
echo "\n----- Testing Listings Endpoint -----\n"
curl -s http://localhost:8000/api/listing/listings/ | python -m json.tool | head -20

# Test Filtering
echo "\n----- Testing Filtering -----\n"
curl -s "http://localhost:8000/api/listing/listings/?exclude_category=sante&exclude_category=avocats" | python -m json.tool | head -20

echo "\n===== Test Complete =====\n"
echo "If you see JSON responses above, your API is working correctly!\n"
echo "For full API documentation, see: listing/api_docs.md\n"
