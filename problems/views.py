from django.views.generic import ListView

from problems.models import Problem


POSTS_PER_PAGE = 2


class ProblemsListView(ListView):
    model = Problem
    paginate_by = POSTS_PER_PAGE
    ordering = ["created_at"]
    template_name = "problems/index.html"
