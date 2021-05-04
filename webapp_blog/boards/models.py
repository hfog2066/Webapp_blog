from django.db import models
import datetime
from django.utils import timezone
# Create your models here

class Users(models.Model):
    id = models.IntegerField(primary_key = True)
    fullname = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    message = models.CharField(max_length = 300)
    pub_date = models.DateTimeField(' date published')

    def __str__(self):
        return self.fullname
    