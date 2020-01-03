from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404

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

    # def create(self, request, *args, **kwargs):
    #     data = {
    #         'user' : request.user.profile.get_absolute_url(),
    #         'content' : request.data.get('content'),
    #         'post' : request.data.get('post'),
    #     }
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class LikeUnlikeView(APIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format = None):
        print('\ncreate like view\n')
        data = {
            'post' : request.data.get('post'),
            'user' : request.user.profile.get_absolute_url(),
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        post_slug = data.get('post')[44:]
        post = get_object_or_404(Post, slug = post_slug)
        data = {}
        if request.user.username in post.get_user_likes():
            post.likes.get(user = request.user).delete()
            data['action'] = 'unlike'
        else:
            Like.objects.create(user = request.user, post = post)
            data['action'] = 'like'
        data['success'] = True
        return Response(data = data)

    # def create(self, request, *args, **kwargs):
    #     data = {
    #         'post' : request.data.get('post'),
    #         'user' : request.user.profile.get_absolute_url(),
    #     }
    #     serializer = self.get_serializer(data = data)
    #     serializer.is_valid(raise_exception = True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class LikeRetrieveView(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class root_view(APIView):
    def get(self, request, format = None):
        return Response({
            'posts': reverse('posts:list', request=request, format=format),
            'users': reverse('profiles:list', request=request, format=format),
        })
