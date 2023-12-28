from django.contrib import admin
from .models import Profile, FriendRequest

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at', )
    search_fields = ('user', )
    
    
@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', )
    searchfields = ('sender', 'receiver', )
