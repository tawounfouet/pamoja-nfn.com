from .downloader import download_to_local

# Try to import Cloudinary helpers, but don't fail if they're not available
try:
    from ._cloudinary import (
        cloudinary_init,
        get_cloudinary_image_object,
        get_cloudinary_video_object,
    )

    cloudinary_available = True
except (ImportError, ModuleNotFoundError):
    # Define a dummy cloudinary_init function if cloudinary is not available
    def cloudinary_init():
        print(
            "Warning: Cloudinary not configured. Image upload functions will not work."
        )

    cloudinary_available = False

# __all__ = ['download_to_local', 'cloudinary_init']

__all__ = [
    "download_to_local",
    "cloudinary_init",
    "get_cloudinary_image_object",
    "get_cloudinary_video_object",
]
