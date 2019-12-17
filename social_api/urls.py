"""social_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt import views as jwt_views
# from rest_framework.authtoken.views import obtain_auth_token
from posts.views import root_view
from profiles.views import UserCreateView, TimelineView, GetProfileView, LoginAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/posts/', include('posts.urls')),
    path('api/users/', include('profiles.urls')),
    path('api/profile/', GetProfileView.as_view(), name = 'profile'),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/auth-token/', obtain_auth_token, name = 'obtain-auth-token'),
    path('api/register/', UserCreateView.as_view(), name = 'register'),
    path('api/login/', LoginAPIView.as_view(), name = 'login'),
    path('api/timeline/', TimelineView.as_view(), name = 'timeline'),
    path('', root_view.as_view(), name = 'root'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
