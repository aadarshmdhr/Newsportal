from django.urls import path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.AdminPostListView.as_view(), name="post-list"),
]