from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("post-by-category/<int:category_id>/", views.PostByCategoryView.as_view(), name="post-by-category"),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
    path("post-by-tag/<int:tag_id>/", views.PostByTagView.as_view(), name="post-by-tag"),
]