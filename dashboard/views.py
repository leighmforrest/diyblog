from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

from blog.models import Blog
from dashboard.forms import BlogForm


class BlogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Blog
    permission_required = 'blog.blogger'
    template_name = "dashboard/index.html"
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        blogger = self.request.user
        return blogger.blogs.all()


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Blog
    template_name = 'dashboard/blog_form.html'
    permission_required = 'blog.blogger'
    form_class = BlogForm
    success_url = reverse_lazy('dashboard:index')
    success_message = 'The blog has been created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = False
        return context

    def form_valid(self, form):
        form.instance.blogger = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Blog
    template_name = "dashboard/blog_form.html"
    permission_required = 'blog.blogger'
    form_class = BlogForm
    success_url = reverse_lazy('dashboard:index')
    success_message = "The blog has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context
    
    def form_valid(self, form):
        form.instance.blogger = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    http_method_names = ['post']
    permission_required = 'blog.blogger'
    success_url = reverse_lazy('dashboard:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        message = f"The blog has been deleted."
        messages.warning(self.request, message)
        return super().delete(request, *args, **kwargs)


