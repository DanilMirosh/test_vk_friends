from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import User, Friendship


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def send_friend_request(request, friend_id):
    """Представления для отправки заявки в друзья"""
    friend = get_object_or_404(User, pk=friend_id)
    if request.user == friend:
        messages.error(request, 'You cannot send a friend request to yourself.')
        return redirect('home')
    friendship, created = Friendship.objects.get_or_create(user1=request.user, user2=friend)
    if not created and friendship.status != 'rejected':
        messages.error(request, 'You have already sent a friend request to this users.')
        return redirect('home')
    messages.success(request, 'Friend request sent to {}.'.format(friend.get_full_name()))
    return redirect('home')
