from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('mod_user.urls')),
    path('accounts/', include('allauth.urls')),
    path('room/', include('mod_space.urls'))
]
