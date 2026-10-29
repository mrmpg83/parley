
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('', lambda request: redirect('/chat/login/')),
    path('admin/', admin.site.urls),
    path('chat/', include('Chat.urls')),
]
