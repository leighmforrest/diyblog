from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls', namespace='pages')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
