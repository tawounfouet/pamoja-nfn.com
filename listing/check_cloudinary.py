#!/usr/bin/env python
"""
Test script to check Cloudinary configuration.
"""
import os
import sys
import django

# Add the project directory to path so Django settings can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings
from helpers._cloudinary.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_PUBLIC_API_KEY,
    CLOUDINARY_SECRET_API_KEY,
)


def check_cloudinary_settings():
    """Check if Cloudinary settings are correctly configured."""
    print("Checking Cloudinary Settings...")
    print("=" * 50)

    # Check if Cloudinary settings are available in Django settings
    print("From Django settings:")
    print(
        f"CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'Not set')}"
    )
    print(
        f"CLOUDINARY_PUBLIC_API_KEY: {getattr(settings, 'CLOUDINARY_PUBLIC_API_KEY', 'Not set')}"
    )
    print(
        f"CLOUDINARY_SECRET_API_KEY: {getattr(settings, 'CLOUDINARY_SECRET_API_KEY', 'Not set')}"
    )
    print(f"CLOUDINARY_URL: {getattr(settings, 'CLOUDINARY_URL', 'Not set')}")
    print("-" * 50)

    # Check values from the cloudinary config module
    print("From cloudinary config module:")
    print(f"CLOUDINARY_CLOUD_NAME: {CLOUDINARY_CLOUD_NAME}")
    print(f"CLOUDINARY_PUBLIC_API_KEY: {CLOUDINARY_PUBLIC_API_KEY}")
    print(f"CLOUDINARY_SECRET_API_KEY: {CLOUDINARY_SECRET_API_KEY}")
    print("=" * 50)

    print("\nEnvironment variables:")
    print(
        f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'Not set in env')}"
    )
    print(
        f"CLOUDINARY_PUBLIC_API_KEY: {os.environ.get('CLOUDINARY_PUBLIC_API_KEY', 'Not set in env')}"
    )
    print(
        f"CLOUDINARY_SECRET_API_KEY: {os.environ.get('CLOUDINARY_SECRET_API_KEY', 'Not set in env')}"
    )
    print(f"CLOUDINARY_URL: {os.environ.get('CLOUDINARY_URL', 'Not set in env')}")

    # Try to initialize cloudinary
    print("\nAttempting to initialize Cloudinary...")
    try:
        from helpers import cloudinary_init

        cloudinary_init()
        print("✅ Cloudinary initialization successful!")
    except Exception as e:
        print(f"❌ Error initializing Cloudinary: {e}")


if __name__ == "__main__":
    check_cloudinary_settings()
