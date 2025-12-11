from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, UpdateView

from django.views.generic import TemplateView

from dashboard.forms import PostForm
from newspaper.models import Post

from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect("/")

class AdminPostListView(StaffRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-published_at")
    

class AdminPostCreateView(StaffRequiredMixin, CreateView):
    model = Post
    template_name = "dashboard/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("dashboard:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class AdminPostDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("dashboard:post-list")
    
class AdminPostUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    template_name = "dashboard/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("dashboard:post-list")