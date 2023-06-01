from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', include('list.urls')),
    path('accounts/', include('allauth.urls')),
]
