from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Secret
from .forms import SecretForm
from django.contrib.auth.decorators import login_required


# Create your views here.
class HomePageView(ListView):
    model = Secret
    context_object_name = 'secrets'
    template_name = 'secret_sharing/home.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SecretForm
        
        return context 
        
        