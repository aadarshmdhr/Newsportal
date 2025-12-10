from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View

from django.views.generic import TemplateView

from dashboard.forms import PostForm
from newspaper.models import Post

# Create your views here.

class AdminPostListView(ListView):
    model = Post
    template_name = "dashboard/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-published_at")
    

class AdminPostCreateView(CreateView):
    model = Post
    template_name = "dashboard/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("dashboard:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class AdminPostDeleteView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("dashboard:post-list")