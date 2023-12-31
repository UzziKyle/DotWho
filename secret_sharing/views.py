from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Secret, Vote
from .forms import SecretForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    context = {}
    
    ordering = request.GET.get('ordering', "")
    secrets = Secret.objects.all()
    
    if ordering:
        secrets = secrets.order_by(ordering)
        
    else:
        secrets = secrets.order_by('-upvote_count')
                
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
    context['ordering'] = ordering
    context['secrets'] = page_obj.object_list
    context['form'] = SecretForm()
    
    if request.method == 'POST':
        form = SecretForm(request.POST)
        
        if form.is_valid():
            secret = form.save(commit=False)
            is_anonymous = request.POST.get('is_anonymous', None)
            
            if is_anonymous:
                secret.author = None
                
            else:
                secret.author = request.user
                                
            secret.save()
            return redirect('home')
        
        else:
            context['form'] = form
                
    return render(request, 'secret_sharing/home.html', context)
            

def view_secret(request, pk):
    context = {}
    
    secret = get_object_or_404(Secret, pk=pk)
    user = request.user
    
    try:
        is_already_voted = Vote.objects.filter(secret=secret, user=user).exists()
    
    except:
        is_already_voted = False
    
    context['title'] = f'{secret.title} | DotWho' if secret.title else f'Secret | DotWho'
    context['secret'] = secret
    context['is_already_voted'] = is_already_voted
    
    return render(request, 'secret_sharing/secret.html', context)


@login_required
def edit_secret(request, pk):
    context = {}
    
    secret = get_object_or_404(Secret, pk=pk)
    
    if secret.author != request.user:
        return redirect('home')
    
    context['title'] = f'{secret.title} | DotWho' if secret.title else f'Secret | DotWho'
    
    if request.method == 'GET':
        context['form'] = SecretForm(instance=secret)

    elif request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        
        if form.is_valid():
            form.save()
            
            return redirect('secret-view', pk=pk)
        
        else:
            context['form'] = form   
            
    return render(request, 'secret_sharing/edit_secret.html', context)
    

@login_required
def upvote(request, pk):
    secret = get_object_or_404(Secret, pk=pk)
    user = request.user
    
    is_already_voted = Vote.objects.filter(secret=secret, user=user).exists()
    
    if not is_already_voted:
        Vote.objects.create(secret=secret, user=user)
        
        secret.upvote_count += 1
        secret.save()
        
    else:
        vote = Vote.objects.get(secret=secret, user=user)
        vote.delete()
        
        secret.upvote_count -= 1
        secret.save()
        
    return redirect('secret-view', pk=secret.pk)
