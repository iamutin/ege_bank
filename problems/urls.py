from django.urls import path

from problems.views import ProblemsListView

app_name = "problems"

urlpatterns = [
    path("", ProblemsListView.as_view(), name="index"),
]
