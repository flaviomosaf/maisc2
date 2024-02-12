from django.db import models
from django.conf import settings
from django.urls import reverse 
from datetime import datetime
from django.contrib.auth.models import User

class Communication(models.Model):

    sender   = models.CharField(max_length=255, null=True, blank=False)
    receiver = models.CharField(max_length=255, null=True, blank=False)
    message  = models.TextField(max_length=255, null=True, blank=True)
    created  = models.DateTimeField(auto_now_add=True)   

    class Meta:
        ordering = ('-created',)      

    def __str__(self):      
        return str(self.created)     

