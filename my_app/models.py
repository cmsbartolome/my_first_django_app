from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
