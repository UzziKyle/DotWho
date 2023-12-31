from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('secret/<int:pk>', views.view_secret, name='secret-view'),
    path('upvote/<int:pk>', views.upvote, name='upvote'),
]
