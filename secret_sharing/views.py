from django.shortcuts import render, redirect
from .models import Secret
from .forms import SecretForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    context = {}
    
    secrets = Secret.objects.all()
    
    context['title'] = 'Home | DotWho'
    context['secrets'] = secrets
    
    if request.method == 'POST':
        form = SecretForm(request.POST)
        
        if form.is_valid():
            secret = form.save(commit=False)
            is_anonymous = request.POST.get('is_anonymous', None)
            if is_anonymous:
                secret.user = None
                
            else:
                secret.user = request.user
                
            secret.save()
            redirect('home')
        
        else:
            context['form'] = form
            return render(request, 'secret_sharing/home.html', context)
        
    context['form'] = SecretForm
        
    return render(request, 'secret_sharing/home.html', context)
            
    # model = Secret
    # context_object_name = 'secrets'
    # template_name = 'secret_sharing/home.html'
    # paginate_by = 3
