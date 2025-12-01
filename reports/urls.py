from django.urls import path

from reports import views

app_name = "reports"

urlpatterns = [
    path("users/", views.UserReportView.as_view(), name="users"),
]