from django.views.generic import ListView, DetailView
from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name='blogs'
    paginate_by = 5


class BlogDetailView(DetailView):
    model = Blog
    template_name='blog/detail.html'
    context_object_name = 'blog'
    