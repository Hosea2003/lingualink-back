from django.urls import path, include
from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns=[
    path('register', views.register_user),
    path('dj-auth/', include('dj_rest_auth.urls')),
    path('dj-auth/registration', include('dj_rest_auth.registration.urls')),
    path('oauth/google/', views.GoogleLogin.as_view()),
    path('validate', views.validate_account),
    path('get-token', views.obtain_token)
]