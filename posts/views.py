from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly


class PostsListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published = True)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class PostDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(published = True)
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly,)


class CommentDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = {
            'user' : request.user.profile.get_absolute_url(),
            'content' : request.data.get('content'),
            'post' : request.data.get('post'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = {
            'post' : request.data.get('post'),
            'user' : request.user.profile.get_absolute_url(),
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class LikeRDView(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class root_view(APIView):
    def get(self, request, format = None):
        return Response({
            'posts': reverse('posts:list', request=request, format=format),
            'users': reverse('profiles:list', request=request, format=format),
        })
