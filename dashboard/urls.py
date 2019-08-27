from django.urls import path

from . import views

app_name= 'dashboard'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='index'),
    path('create/', views.BlogCreateView.as_view(), name='create_blog'),
    path('<slug:slug>/update/', views.BlogUpdateView.as_view(), name='update_blog'),
    path('<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),
]
