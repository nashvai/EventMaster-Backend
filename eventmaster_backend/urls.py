"""
URL configuration for eventmaster_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from Eventmaster.views import RegisterUserViewSet  # Make sure to import your RegisterUserViewSet
from rest_framework_simplejwt import views as jwt_views

# Initialize your router and register the User view
router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='user')



urlpatterns = [
    path("admin/", admin.site.urls),
     path('api/', include('Eventmaster.urls')),  # Ensure your app's URLs are included
     path('api/', include(router.urls)), 
     # Route to obtain a new access and refresh token
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Route to refresh the access token using a valid refresh token
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
