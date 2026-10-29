from django.urls import path
from .views import index, login_view, logout_view, room

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<str:room_name>/', room, name='room'),
]