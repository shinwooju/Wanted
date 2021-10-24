from django.db   import models
from core.models import TimeStamp


class User(TimeStamp):
    name     = models.CharField(max_length = 16)
    email    = models.CharField(max_length = 128)
    password = models.CharField(max_length = 512)
    
    class Meta:
        db_table = 'users'