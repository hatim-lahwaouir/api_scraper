from django.urls import path
from .views import login,signUp


urlpatterns = [
    
    path('login/', login),
    path('sign-up/', signUp),
]
