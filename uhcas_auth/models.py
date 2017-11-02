'''
Use django user model 
'''
from django.db import models
from django.contrib.auth.models import User

class UHCASUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    common_name = models.CharField(max_length=128, blank=True, null=True)
    display_name = models.CharField(max_length=128, blank=True, null=True)
    affiliation = models.CharField(max_length=254, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
