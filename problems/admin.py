from django.contrib import admin
from problems.models import Problem, MatchLeftOption, MatchRightOption, MatchPair


class MatchLeftOptionInline(admin.TabularInline):
    model = MatchLeftOption
    extra = 0


class MatchRightOptionInline(admin.TabularInline):
    model = MatchRightOption
    extra = 0


class MatchPairInline(admin.TabularInline):
    model = MatchPair
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ограничиваем список вариантов слева и справа только текущей задачей.
        """
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Определяем, какая задача редактируется
        obj_id = request.resolver_match.kwargs.get("object_id")
        if obj_id:
            if db_field.name == "left_option":
                field.queryset = MatchLeftOption.objects.filter(problem_id=obj_id)
            elif db_field.name == "right_option":
                field.queryset = MatchRightOption.objects.filter(problem_id=obj_id)

        return field


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("number", "task_type", "created_at", "show_pairs")
    inlines = [MatchLeftOptionInline, MatchRightOptionInline, MatchPairInline]
    list_filter = ("task_type", "created_at")
    search_fields = ("number", "text")

    def show_pairs(self, obj):
        pairs = obj.pairs.all()
        if not pairs:
            return "—"
        return ", ".join(f"{p.left_option.label} → {p.right_option.index}" for p in pairs)
    show_pairs.short_description = "Соответствия"
