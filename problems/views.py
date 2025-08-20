from django.views.generic import ListView

from problems.models import Problem

POSTS_PER_PAGE = 3


class ProblemsListView(ListView):
    model = Problem
    paginate_by = POSTS_PER_PAGE
    ordering = ["created_at"]
    template_name = "problems/index.html"

    def get_queryset(self):
        return super().get_queryset().select_related(
        ).prefetch_related(
            'match_options',
            'match_answer_options',
        )
