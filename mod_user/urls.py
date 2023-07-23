from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('register', views.register_user),
    path('dj-auth/', include('dj_rest_auth.urls')),
    path('dj-auth/registration', include('dj_rest_auth.registration.urls')),
    path('oauth/google/', views.GoogleLogin.as_view()),
    path('validate', views.validate_account),
    path('get-token/', views.obtain_token),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('get-users', views.get_users),
    path('get-users-by-email', views.get_user_email),
    path('get-users-by-username', views.get_user_username),
    path('send-code', views.get_validation_code)
]