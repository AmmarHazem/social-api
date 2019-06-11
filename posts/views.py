from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly


class PostsListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published = True)

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

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user = self.request.user, created = datetime.now())
        return serializer.save(created = datetime.now())


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user = self.request.user, created = datetime.now())
        return serializer.save(created = datetime.now())


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
