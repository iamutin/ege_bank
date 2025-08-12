from django.contrib import admin, messages
from django import forms
from .models import Problem, MatchOption, MatchAnswerOption
from .forms import MatchOptionFormSet, MatchAnswerOptionFormSet


class ProblemAdminForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = "__all__"


class MatchAnswerOptionInline(admin.TabularInline):
    model = MatchAnswerOption
    formset = MatchAnswerOptionFormSet
    extra = 4
    max_num = 4
    min_num = 4
    readonly_fields = ("label",)  # метка только для чтения

    def has_delete_permission(self, request, obj=None):
        return False


class MatchOptionInline(admin.TabularInline):
    model = MatchOption
    formset = MatchOptionFormSet
    extra = 2
    max_num = 2
    min_num = 2
    readonly_fields = ("label",)  # метка только для чтения

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    form = ProblemAdminForm

    list_display = ("number", "task_type", "created_at")
    list_filter = ("task_type",)
    search_fields = ("number", "text")

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        if obj.task_type == "match":
            return [
                MatchAnswerOptionInline(self.model, self.admin_site),
                MatchOptionInline(self.model, self.admin_site),
            ]

        return []

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)

        if obj and obj.task_type == "match":
            has_answers = MatchAnswerOption.objects.filter(problem=obj).exists()
            has_options = MatchOption.objects.filter(problem=obj).exists()

            if not (has_answers and has_options):
                self.message_user(
                    request,
                    "💡 Для задания на соответствие сначала сохраните задачу, затем заполните варианты ответа и соответствия.",
                    level=messages.WARNING,
                )

        return super().change_view(request, object_id, form_url, extra_context)
