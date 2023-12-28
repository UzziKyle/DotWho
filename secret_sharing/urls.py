from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('secret/<int:id>', views.secret_detail, name='secret_detail'),
]
