from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
# from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from knox.models import AuthToken

from .models import Profile
from .permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer, ProfileDetailSerializer, UserCreateSerializer, LoginSerializer, ProfileImageSerializer
from posts.serializers import PostSerializer


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        if isinstance(user, User):
            return Response({
                'user': ProfileSerializer(user.profile, context = self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user)[1],
            })
        return Response({
            'detail' : 'Incorrect username or password',
            'status' : 400,
        }, status = status.HTTP_400_BAD_REQUEST)


class GetProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format = None):
        ser_profile = ProfileDetailSerializer(request.user.profile, context = {'request' : request})
        return Response(ser_profile.data)


class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format = None):
        follow_user = User.objects.get(username = request.data.get('user'))
        if request.data['action'] == 'follow':
            self.request.user.profile.following.add(follow_user)
        elif request.data['action'] == 'unfollow':
            self.request.user.profile.following.remove(follow_user)
        return Response({'success' : True}, status = 200)


class TimelineView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.profile.get_timeline()


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        valid_data = serializer.validated_data
        return User.objects.create_user(valid_data['username'], valid_data.get('email', ''), valid_data['password1'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = AuthToken.objects.create(user)[1]
        data = {
            'user' : ProfileSerializer(user.profile, context = self.get_serializer_context()).data,
            'token' : token,
            }
        return Response(data, headers = headers, status = status.HTTP_201_CREATED)


class UserRetrieveView(generics.RetrieveUpdateAPIView):
    lookup_field = 'username'
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
