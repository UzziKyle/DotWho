from django.contrib import admin
from .models import Secret

# Register your models here.
@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_anonymous', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user')
    