import cloudinary
import os
from django.conf import settings

# Try to get Cloudinary settings from Django settings, otherwise use defaults or environment variables
try:
    CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
    CLOUDINARY_PUBLIC_API_KEY = settings.CLOUDINARY_PUBLIC_API_KEY
    CLOUDINARY_SECRET_API_KEY = settings.CLOUDINARY_SECRET_API_KEY
except AttributeError:
    # Fallback to environment variables or default values
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "default_cloud_name")
    CLOUDINARY_PUBLIC_API_KEY = os.environ.get(
        "CLOUDINARY_PUBLIC_API_KEY", "default_public_api_key"
    )
    CLOUDINARY_SECRET_API_KEY = os.environ.get(
        "CLOUDINARY_SECRET_API_KEY", "default_secret_api_key"
    )

# Configuration
# cloudinary.config(
#     cloud_name = "dsz3haz29",
#     api_key = "your_api_key",
#     api_secret = "<your_api_secret>", # Click 'View API Keys' above to copy your API secret
#     secure=True
# )


def cloudinary_init():
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_PUBLIC_API_KEY,
        api_secret=CLOUDINARY_SECRET_API_KEY,
        secure=True,
    )
