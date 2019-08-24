from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls', namespace='pages')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
