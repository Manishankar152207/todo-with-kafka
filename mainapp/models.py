from django.db import models
from api.models import CommonFields
from django.contrib.auth.models import User
# Create your models here.
class ActivityFeed(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    data = models.JSONField()
    
    def __str__(self) -> str:
        return self.user.username
