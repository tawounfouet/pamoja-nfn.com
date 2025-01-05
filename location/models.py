from django.db import models

# Create your models here.

#PARIS_COORDINATES = {"lat": 48.8566, "lng": 2.3522}

def get_default_coordinates():
    return {"lat": 48.8566, "lng": 2.3522}


class Location(models.Model):
    coordinates = models.JSONField(    
        null=True, 
        blank=True,
        #default=None,
        #default=PARIS_COORDINATES,
        default=get_default_coordinates,

        help_text="Coordinates in {lat: float, lng: float} format")
      # {lat: float, lng: float}
    address = models.TextField(blank=True, null=True, default=None)
    city = models.CharField(max_length=100, blank=True, null=True, default="Paris")
    postal_code = models.CharField(max_length=10, blank=True, null=True, default="75000")
    region = models.CharField(max_length=100, blank=True, null=True, default="Île-de-France")
    country = models.CharField(max_length=100, blank=True, null=True, default="France")

    def __str__(self):
        return f"{self.city}, {self.country}"