from django.db import models
from django.contrib.auth.models import User


def profile_directory_path(instance, filename) -> str: 
    ext = filename.split('.')[-1]
    filename = f'{instance.id : 04d}_{instance.user.username}.{ext}'
    
    return f'profile_pictures/{filename}'


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        abstract = True
        
        
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to=profile_directory_path, blank=True)
    bio = models.TextField(max_length=120, blank=True, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    
    def __str__(self) -> str:
        return f'Profile of {self.user.username}'
    
    @property
    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            
            return self.photo.url
        
        return "/media/profile_pictures/default.jpg"
    

class FriendRequest(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', null=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=False)
    
    def __str__(self) -> str:
        return f'Friend request from {self.sender.username} to {self.receiver.username}'
    