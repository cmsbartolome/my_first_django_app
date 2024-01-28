from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    ordering = ['-id']
    STATUS = (
    ('Active','active'),
    ('In-active','in-active')
    )
    title = models.TextField(max_length=160, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='user', on_delete=models.SET_NULL, null=True)
    createdOn = models.DateTimeField(auto_now_add=True, null=True)
    updatedOn = models.DateTimeField(auto_now=False, null=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    
    
    def __str__(self):
         return self.title
    
    # @property 
    # def author(self):
    #     return self.createdBy.username

