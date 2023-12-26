from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Secret(models.Model):
    title = models.CharField(max_length=60, blank=True, null=False)
    content = models.TextField(max_length=280, blank=False, null=False)
    is_anonymous = models.BooleanField(default=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        if self.title:
            return f'{self.id} | {self.title}'
        
        return f'{self.id} | no title'
    