from django.urls import path

from . import views

app_name= 'blog'

urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('<slug:slug>', views.BlogDetailView.as_view(), name='detail'),
    #path('<slug:slug>/create', views.BlogDetailView.as_view(), name='detail'),
]
