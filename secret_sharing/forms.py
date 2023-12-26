from django import forms
from .models import Secret


class SecretForm(forms.ModelForm):
    class Meta:
        model = Secret
        fields = ['title', 'content', 'is_anonymous']
        