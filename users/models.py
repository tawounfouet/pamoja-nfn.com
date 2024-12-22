from django.db import models
from django.db.models.signals import post_save


from authentication.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True) 
    address = models.CharField(max_length=200, null=True, blank=True) 
    country = models.CharField(max_length=200, null=True, blank=True) 
    verified = models.BooleanField(default=False, null=True, blank=True)

    
    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"
    
    @property
    def get_profile_image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/default_profile.png' 
    


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User) 