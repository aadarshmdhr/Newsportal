from django.http import JsonResponse
from django.shortcuts import render

from newspaper.models import Advertisement, Post, Contact, Category, OurTeam, Tag

from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.utils import timezone
from datetime import timedelta
from django.views.generic.edit import FormMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from newspaper.forms import CommentForm, ContactForm, NewsletterForm


# Create your views here.

class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context


class HomeView(SidebarMixin, TemplateView):
    template_name = "newsportal/home.html"


    # If we want to send extra data to the template we use get_context_data

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

        return context
    

class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
    

class PostDetailView(SidebarMixin, FormMixin, DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        
        return query
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comment = form.save(commit=False)
        # comment.post = self.object
        comment.user = self.request.user
        comment.save()
        messages.success(self.request, "Your comment has been added successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your comment. Please check the form."
        )
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        current_post = self.object
        current_post.view_count += 1
        current_post.save()

        context["related_articles"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                category=self.object.category,
            )
            .exclude(id=self.object.id)
            .order_by("-published_at", "-view_count")[:2]
        )
        return context
    
class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error sending your message. Please check the form.",
        )
        return super().form_invalid(form)
    
class CategoryListView(ListView):
    model = Category
    template_name = "newsportal/categories.html"
    context_object_name = "categories"

class AboutView(TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context
    
def tags(request):
    all_tags = Tag.objects.all()
    return render(
        request,
        "tags.html",
        {"tags": all_tags}
    )

class PostByCategoryView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category_id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query
    
class NewsletterView(View):
    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                    "success": True,
                    "message": "Successfully subscribed to the newsletter.",
                },
                status = 201,
                )
            else:
                print(form.errors)
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status = 400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                },
                status = 400,
            )