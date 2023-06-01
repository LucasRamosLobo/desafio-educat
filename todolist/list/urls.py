from django.urls import path, include
from . import views

app_name = 'list'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
