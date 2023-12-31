from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        abstract = True


class Secret(BaseModel):
    title = models.CharField(max_length=60, blank=True, null=False)
    content = models.TextField(max_length=280, blank=False, null=False)
    is_anonymous = models.BooleanField(default=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='secret')
    upvote_count = models.IntegerField(default=0)
    comments = GenericRelation(Comment)
    
    def __str__(self) -> str:
        if self.title:
            if self.is_anonymous:
                return f'{self.id} | {self.title} | @anonymous'
            
            return f'{self.id} | {self.title} | @{self.author.username}'
        
        else:
            if self.is_anonymous:
                return f'{self.id} | no title | @anonymous'
            
            return f'{self.id} | no title | @{self.author.username}'
    
    
class Vote(BaseModel):
    secret = models.ForeignKey(Secret, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'Vote of {self.user.username} to {self.secret}'
    