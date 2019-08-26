from django.urls import path

from . import views

app_name= 'dashboard'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='dashboard'),
    path('<slug:slug>/update/', views.UpdateBlogView.as_view(), name='update_blog'),
    path('<slug:slug>/delete/', views.DeleteBlogView.as_view(), name='delete_blog'),
]
