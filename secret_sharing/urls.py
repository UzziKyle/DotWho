from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('secret/<int:pk>', views.view_secret, name='secret-view'),
    path('secret/<int:pk>/edit', views.edit_secret, name='secret-edit'),
    path('secret/<int:pk>/delete', views.delete_secret, name='secret-delete'),
    path('upvote/<int:pk>', views.upvote, name='upvote'),
]
