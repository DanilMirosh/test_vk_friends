from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, FriendRequestResponseSerializer, \
    UserRegistrationSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    # permission_classes = (IsAuthenticated,)


class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class FriendRequestRespondView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestResponseSerializer
    # permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == FriendRequest.ACCEPTED:
            instance.to_user.friends.add(instance.from_user)
            instance.from_user.friends.add(instance.to_user)
        elif instance.status == FriendRequest.REJECTED:
            pass


class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status=FriendRequest.PENDING)


class FriendListView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        friends = user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)
