from django.urls import path

from . import views

app_name= 'blog'

urlpatterns = [
    path('blogs/', views.BlogListView.as_view(), name='blog'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/create/', views.CreateCommentView.as_view(), name='create_comment'),
    path('<int:pk>/update/', views.UpdateCommentView.as_view(), name='update_comment'),
    path('<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
]
