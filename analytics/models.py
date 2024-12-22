# analytics/models.py
from django.utils import timezone
from django.db import models

class PageView(models.Model):
    ip_address = models.CharField(max_length=45)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    loc = models.CharField(max_length=50, null=True, blank=True)
    org = models.CharField(max_length=255, null=True, blank=True)
    postal = models.CharField(max_length=20, null=True, blank=True)
    timezone_info = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    page_requested = models.CharField(max_length=255)
    #viewed_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(default=timezone.now)
    first_time_view = models.DateTimeField(default=timezone.now)
    last_time_viewed = models.DateTimeField(default=timezone.now)
    
    view_count = models.IntegerField(default=0)  # New field for view count

    referrer = models.CharField(max_length=255, null=True, blank=True)  # Add this field


    def __str__(self):
        return f'{self.ip_address} - {self.page_requested}'
