from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
import json

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        if username:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()
            login(request, user)
            return redirect('index')

    return render(request, 'Chat/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'Chat/index.html', {'username': request.user.username})


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect('login')

    username = request.user.username
    context = {
        'room_name': room_name,
        'username': mark_safe(json.dumps(username))
    }
    return render(request, "Chat/room.html", context)