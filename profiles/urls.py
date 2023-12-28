from django.urls import path
from . import views


urlpatterns = [
    # authentication
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    
    # profile viewing and editing
    path('profile/?P<int:pk>/', views.view_profile, name='profile-view'),
    path('profile/?P<int:pk>/edit/', views.edit_profile, name='profile-edit'),
    
    # friend requesting
    path('profile/?P<int:pk>/add/', views.add_friend, name='add-friend'),
    path('profile/?P<int:pk>/add/decline', views.decline_friend_request, name='decline-friend-request'),
    path('profile/?P<int:pk>/add/accept', views.accept_friend_request, name='accept-friend-request'),
    path('profile/?P<int:pk>/remove/', views.remove_friend, name='remove-friend'),
    
    # friends viewing
    path('friends/', views.view_friends, name='view-friends')
]
