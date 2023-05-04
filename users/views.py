from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import FriendRequest, Friend
from django.contrib.auth.models import User


@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user
    )
    return redirect('profile', user_id=user.id)


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        friend_request.accepted = True
        friend_request.save()
        friend = Friend.objects.create(user=request.user, friend=friend_request.from_user)
        Friend.objects.create(user=friend_request.from_user, friend=request.user)
        return redirect('profile', user_id=request.user.id)
    return render(request, 'friend_request.html', {'friend_request': friend_request})


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        friend_request.delete()
        return redirect('profile', user_id=request.user.id)
    return render(request, 'friend_request.html', {'friend_request': friend_request})


@login_required
def friend_requests(request):
    friend_requests_received = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, 'friend_requests.html',
                  {'friend_requests_received': friend_requests_received, 'friend_requests_sent': friend_requests_sent})


@login_required
def friends(request):
    friends = Friend.objects.filter(user=request.user)
    return render(request, 'friends.html', {'friends': friends})


@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(Friend, user=request.user, friend__id=friend_id)
    if request.method == 'POST':
        friend.delete()
        reverse_friend = get_object_or_404(Friend, user=friend.friend, friend=request.user)
        reverse_friend.delete()
        return redirect('profile', user_id=request.user.id)
    return render(request, 'remove_friend.html', {'friend': friend})
