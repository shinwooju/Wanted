from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('users', include('users.urls')),
    path('posts', include('posts.urls')),
    path('admin/', admin.site.urls)
]
