from django.urls import path, re_path
from posts import views


app_name = 'posts'

urlpatterns = [
    re_path('^$', views.PostsListView.as_view(), name = 'list'),
    path('post-comment/', views.CommentCreate.as_view(), name = 'create-comment'),
    path('<slug:slug>', views.PostDetailUpdateDestroyView.as_view(), name = 'detail'),
    path('comment/<int:pk>', views.CommentDetailUpdateDestroyView.as_view(), name = 'comment'),
    path('like/<int:pk>', views.LikeRDView.as_view(), name = 'like'),
    path('like/', views.CreateLikeView.as_view(), name = 'create-like'),
]