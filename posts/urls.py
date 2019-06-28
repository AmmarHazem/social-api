from django.urls import path, re_path
from posts import views


app_name = 'posts'

urlpatterns = [
    re_path('^$', views.PostsListView.as_view(), name = 'list'),
    path('post-comment/', views.CommentCreate.as_view(), name = 'create-comment'),
    path('<slug:slug>', views.PostDetailUpdateDestroyView.as_view(), name = 'detail'),
    path('comment/<int:pk>', views.CommentDetailUpdateDestroyView.as_view(), name = 'comment'),
    re_path(r'^like/$', views.LikeUnlikeView.as_view(), name = 'like-unlike'),
    path('like/<int:pk>', views.LikeRetrieveView.as_view(), name = 'like'),
]