from django.shortcuts import render
from django.views.generic import ListView

from django.views.generic import TemplateView

from newspaper.models import Post

# Create your views here.

class AdminPostListView(ListView):
    model = Post
    template_name = "dashboard/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-published_at")