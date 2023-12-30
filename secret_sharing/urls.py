from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('secret/<int:pk>', views.secret_detail, name='secret_detail'),
    path('upvote/<int:pk>', views.upvote, name='upvote'),
]
