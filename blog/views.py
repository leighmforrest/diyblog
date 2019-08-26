from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from .models import Blog, Comment, PERM
from .forms import CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name='blogs'
    paginate_by = 5


class BlogDetailView(DetailView):
    model = Blog
    template_name='blog/detail.html'
    context_object_name = 'blog'


class BloggerListView(ListView):
    context_object_name = 'bloggers'
    template_name = 'blog/bloggers.html'

    def get_queryset(self):
        return get_user_model().objects.filter(Q(user_permissions=PERM) | Q(is_superuser=True)).distinct()


class BloggerDetailView(DetailView):
    context_object_name = 'blogger'
    template_name = 'blog/blogger.html'
    
    def get_queryset(self):
        return get_user_model().objects.filter(Q(user_permissions=PERM) | Q(is_superuser=True), pk=self.kwargs['pk'])


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs['slug']])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.blog = Blog.objects.get(slug=str(self.kwargs['slug']))
        return super().form_valid(form)


class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def get_success_url(self):
        comment = self.get_object()
        return comment.blog.get_absolute_url()

    def form_valid(self, form):
        comment = self.get_object()
        form.instance.user = self.request.user
        form.instance.blog = comment.blog
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete.html'

    def get_success_url(self):
        comment = self.get_object()
        return comment.blog.get_absolute_url()
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)