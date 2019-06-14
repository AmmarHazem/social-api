from rest_framework import serializers
from .models import Post, Comment, Like


user_kwargs = {
    'view_name' : 'profiles:user-detail',
    'lookup_field' : 'username',
}


class PostSerializer(serializers.HyperlinkedModelSerializer):

    comments = serializers.HyperlinkedRelatedField(view_name = 'posts:comment', many = True, read_only = True)
    likes = serializers.HyperlinkedRelatedField(view_name = 'posts:like', many = True, read_only = True)
    # user = serializers.ReadOnlyField(source = 'user.username')

    class Meta:
        model = Post
        fields = ('url', 'title', 'slug', 'content', 'user', 'published', 'created', 'comments', 'likes')
        extra_kwargs = {
            'url' : {
                'view_name' : 'posts:detail',
                'lookup_field' : 'slug',
            },
            'user' : user_kwargs,
        }


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    # created = serializers.DateTimeField(auto_now_add = True, required = False)

    class Meta:
        model = Comment
        fields = ('content', 'post', 'user', 'created')
        extra_kwargs = {
            'post' : {
                'view_name' : 'posts:detail',
                'lookup_field' : 'slug',
            },
            'user' : user_kwargs,
        }


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user', 'created')
        extra_kwargs = {
            'post' : {
                'view_name' : 'posts:detail',
                'lookup_field' : 'slug',
            },
            'user' : user_kwargs,
        }
