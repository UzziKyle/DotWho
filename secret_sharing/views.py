from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Secret
from .forms import SecretForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    context = {}
    
    ordering = request.GET.get('ordering', "")
    secrets = Secret.objects.all()
    
    if ordering:
        secrets = secrets.order_by(ordering)
        
    paginator = Paginator(secrets, 3)
    page_number = request.GET.get("page")
    
    try:
        page_obj = paginator.get_page(page_number)
        
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context['title'] = 'Home | DotWho'
    context['paginator'] = paginator
    context['page_obj'] = page_obj
    context['secrets'] = page_obj.object_list
    context['form'] = SecretForm()
    
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
            return redirect('home')
        
        else:
            context['form'] = form
                
    return render(request, 'secret_sharing/home.html', context)
            
