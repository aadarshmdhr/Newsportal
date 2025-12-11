from django.urls import path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.AdminPostListView.as_view(), name="post-list"),
    path("post-create/", views.AdminPostCreateView.as_view(), name="post-create"),
    path("post-delete/<int:pk>/", views.AdminPostDeleteView.as_view(), name="post-delete"),
    path("post-update/<int:pk>/", views.AdminPostUpdateView.as_view(), name="post-update"),
]