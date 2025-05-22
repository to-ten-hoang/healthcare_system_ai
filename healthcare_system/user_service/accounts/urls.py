from django.urls import path
from .views import RegisterView, AdminRegisterView, UserProfileView, UserInfoView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-admin/', AdminRegisterView.as_view(), name='register-admin'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('users/', UserListView.as_view(), name='user-list'),  # Endpoint mới cho admin
]