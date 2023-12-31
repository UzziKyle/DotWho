from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, FriendRequest
from secret_sharing.models import Secret, Vote
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm, ProfileForm


# Create your views here.
def sign_in(request):
    context = {}
    
    next_action = request.GET.get('next', "")
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        
        context['form'] = LoginForm()
        context['next_action'] = next_action
            
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                
                if next_action:
                    return redirect(next_action)
                
                return redirect('home')
            
        context['form'] = form
            
    return render(request, 'profiles/login.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')


def sign_up(request):
    context = {}
    
    if request.method == 'GET':
        context['form'] = RegistrationForm()

    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            return redirect('home')
        
        context['form'] = form
        
    return render(request, 'profiles/register.html', context)

      
@login_required  
def view_profile(request, pk):
    context = {}
    user = get_object_or_404(User, pk=pk)
    profile = user.profile if hasattr(user, 'profile') else None
    
    is_a_friend = request.user in profile.friends.all() if profile else False
    
    try:
        has_requested_to = FriendRequest.objects.get(receiver=user, sender=request.user)
    except:
        has_requested_to = False
    
    try:
        is_requested_by = FriendRequest.objects.get(receiver=request.user, sender=user)
    except:
        is_requested_by = False
        
    authored_secrets = Secret.objects.filter(author=user).order_by('-created_at')[:3]
    
    liked_secrets = Vote.objects.filter(user=user).order_by('-created_at')[:3]
    liked_secrets = liked_secrets.values_list('secret', flat=True)
    liked_secrets = Secret.objects.filter(pk__in=set(liked_secrets))
    
    try:
        friends = profile.friends.all()[:3]
    
    except:
        friends = None
        
    context['title'] = f'{user.username} | DotWho'
    context['user'] = user
    context['profile'] = profile
    context['is_a_friend'] = is_a_friend
    context['has_requested_to'] = has_requested_to
    context['is_requested_by'] = is_requested_by
    context['friends'] = friends
    context['authored_secrets'] = authored_secrets
    context['liked_secrets'] = liked_secrets
    
    return render(request, 'profiles/profile.html', context)


@login_required   
def edit_profile(request, pk):
    context = {}
    
    user = get_object_or_404(User, pk=pk)
    profile = user.profile if hasattr(user, 'profile') else None
    
    context['title'] = f'{user.username} | DotWho'
    
    if request.method == 'GET':
        context['form'] = ProfileForm(instance=profile)
    
    elif request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            
            return redirect('profile-view', pk=pk)

        else:
            context['form'] = form
    
    return render(request, 'profiles/edit_profile.html', context)


@login_required
def add_friend(request, pk):
    sender = request.user
    receiver = User.objects.get(pk=pk)
    friend_request = FriendRequest(sender=sender, receiver=receiver)
    
    friend_request.save()
    
    return redirect('profile-view', pk=pk)


@login_required
def decline_friend_request(request, pk):
    receiver = request.user
    sender = User.objects.get(pk=pk)
    
    friend_request = FriendRequest.objects.get(receiver=receiver, sender=sender)
    
    friend_request.delete()
    
    return redirect('profile-view', pk=pk)
    
    
@login_required
def accept_friend_request(request, pk):
    receiver = request.user
    sender = User.objects.get(pk=pk)
    
    receiver_profile = receiver.profile if hasattr(receiver, 'profile') else None    
    sender_profile = sender.profile if hasattr(sender, 'profile') else None   
     
    receiver_profile.friends.add(sender)
    sender_profile.friends.add(receiver)
    
    friend_request = FriendRequest.objects.get(receiver=receiver, sender=sender)
    
    friend_request.delete()
    return redirect('profile-view', pk=pk)


@login_required
def remove_friend(request, pk):
    receiver = request.user
    sender = User.objects.get(pk=pk)
    
    receiver_profile = receiver.profile if hasattr(receiver, 'profile') else None    
    sender_profile = sender.profile if hasattr(sender, 'profile') else None   
     
    receiver_profile.friends.remove(sender)
    sender_profile.friends.remove(receiver)
    
    return redirect('profile-view', pk=pk)


@login_required
def view_friends(request):
    context = {}
    
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None
    
    friends = profile.friends.all()
    
    paginator = Paginator(friends, 3)
    page_number = request.GET.get("page")
    
    try:
        page_obj = paginator.get_page(page_number)
        
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    friend_requests_received = FriendRequest.objects.filter(receiver=user).order_by('-created_at')[:5]  # Retrieves the five latest friend requests received
    friend_requests_received = friend_requests_received.values_list('sender', flat=True)  # Gets the senders ids
    friend_requests_received = User.objects.filter(pk__in=set(friend_requests_received))    
    
    friend_requests_sent = FriendRequest.objects.filter(sender=user).order_by('-created_at')[:5]  # Retrieves the five latest friend requests sent
    friend_requests_sent = friend_requests_sent.values_list('receiver', flat=True)  # Gets the receivers ids
    friend_requests_sent = User.objects.filter(pk__in=set(friend_requests_sent))
    
    context['title'] = f'Friends | DotWho'
    context['paginator'] = paginator
    context['page_obj'] = page_obj
    context['friends'] = page_obj.object_list
    context['friend_requests_received'] = friend_requests_received
    context['friend_requests_sent'] = friend_requests_sent
    
    return render(request, 'profiles/friends.html', context)
    