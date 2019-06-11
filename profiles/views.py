from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Profile
from .serializers import ProfileSerializer, ProfileDetailSerializer, UserCreateSerializer
from posts.serializers import PostSerializer


class FollowUnfollowView(APIView):
    def post(self, request, format = None):
        follow_user = User.objects.get(username = request.data.get('user'))
        if request.data['action'] == 'follow':
            self.request.user.profile.following.add(follow_user)
        elif request.data['action'] == 'unfollow':
            self.request.user.profile.following.remove(follow_user)
        return Response({'success' : True}, status = 200)


class TimelineView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.request.user.profile.get_timeline()


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserCraeteView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        valid_data = serializer.validated_data
        User.objects.create_user(valid_data['username'], valid_data.get('email', ''), valid_data['password1'])
        serializer.data['password1'] = ''
        serializer.data['password2'] = ''


class UserRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
