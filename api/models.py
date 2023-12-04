from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CommonFields(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Task(CommonFields):
    name = models.CharField(max_length=255)
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_tasks", null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        unique_together = ["name", "user"] 
