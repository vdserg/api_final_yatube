from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from api.views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

v1_router = DefaultRouter()
v1_router.register('posts', viewset=PostViewSet)
v1_router.register(r'posts/(?P<post_id>\d+)/comments',
                   viewset=CommentViewSet,
                   basename='comments')
v1_router.register('group', viewset=GroupViewSet)
v1_router.register('follow', viewset=FollowViewSet, basename='follow')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh')
]
