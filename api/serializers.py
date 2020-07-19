from rest_framework import serializers

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')

    def validate(self, attrs):
        data = self.initial_data
        user = self.context.get('request').user
        if 'following' not in data:
            raise serializers.ValidationError("Following field can't be empty")
        elif User.objects.filter(username=data['following']).exists():
            following = User.objects.get(username=data['following'])
        else:
            raise serializers.ValidationError(
                "User matching following don't exist")
        if user == following:
            raise serializers.ValidationError("User can't follow himself")
        if user.following.filter(following=following).exists():
            raise serializers.ValidationError(
                "User can't follow same author twice")
        return data

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
