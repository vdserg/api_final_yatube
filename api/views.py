from rest_framework import viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly

from api.permissions import IsOwnerOrReadOnly
from api.serializers import PostSerializer, CommentSerializer, \
    GroupSerializer, FollowSerializer
from .models import Post, Group, Follow


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_fields = ['group']

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments

    def perform_create(self, serializer):
        get_object_or_404(Post, id=self.kwargs['post_id'])
        return serializer.save(author=self.request.user)


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet,):

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) # тестами требуется вернуть статус 200 без токена, поэтому сделал get_queryset
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Follow.objects.all()
        else:
            return []
