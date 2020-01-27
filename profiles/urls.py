from django.urls import path, re_path
from profiles import views


app_name = 'profiles'

urlpatterns = [
    re_path('^$', views.ProfileListView.as_view(), name = 'list'),
    path('follow-unfollow/', views.FollowUnfollowView.as_view(), name = 'follow-unfollow'),
    path('<str:username>/', views.UserRetrieveUpdateView.as_view(), name = 'user-detail'),
]
