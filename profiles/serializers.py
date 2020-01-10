from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from .models import Profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 300)
    password1 = serializers.CharField(style={'input_type': 'password'}, max_length = 200)
    password2 = serializers.CharField(style={'input_type': 'password'}, max_length = 200)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords did not match')
        return data

    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'], '', validated_data['password1'])

    # def update(self, instance, validated_data):
    #     instance.password = validated_data.get('code', instance.code)
    #     instance.save()
    #     return instance


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    followers = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'profiles:user-detail',
        lookup_field = 'username',
        many = True,
        source = 'user.followers',
    )

    username = serializers.CharField(max_length = 200, source = 'user.username', read_only = True)

    class Meta:
        model = Profile
        fields = ('user', 'name', 'username', 'image', 'bio', 'following', 'followers', 'created',)
        extra_kwargs = {
            'following' : {
                'view_name' : 'profiles:user-detail',
                'lookup_field' : 'username',
            },
            'user' : {
                'view_name' : 'profiles:user-detail',
                'lookup_field' : 'username',
                'read_only': True,
            },
        }


class ProfileDetailSerializer(serializers.HyperlinkedModelSerializer):

    followers = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'profiles:user-detail',
        lookup_field = 'username',
        many = True,
        source = 'user.followers',
    )

    posts = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'posts:detail',
        lookup_field = 'slug',
        many = True,
        source = 'user.posts',
    )

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image', 'created', 'following', 'followers', 'posts',)
        extra_kwargs = {
            'following' : {
                'view_name' : 'profiles:user-detail',
                'lookup_field' : 'username',
            },
        }


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)
