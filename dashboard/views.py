from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from blog.models import PERM


class BlogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Blog
    permission_required = PERM
    template_name = "dashboard/index.html"


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'dashboard/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BlogDeleteView(DeleteView):
    model = Blog
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


