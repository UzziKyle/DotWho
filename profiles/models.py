from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        abstract = True
        
        
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=120, blank=True)
    
    def __str__(self) -> str:
        return f'Profile of {self.user.username}'