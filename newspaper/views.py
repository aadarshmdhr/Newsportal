from django.shortcuts import render

from newspaper.models import Post

from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta


# Create your views here.


class HomeView(TemplateView):
    template_name = "newsportal/home.html"


    # If we want to send extra data to the template we user get_context_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breaking_news"] = Post.objects.filter(
            published_at__isnull=False, status="active", is_breaking_news=True
        ).order_by("-published_at")[:3]

        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-view_count")
            .first()
        )

        context["trending_news"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["week_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-view_count")[:5]

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        return context