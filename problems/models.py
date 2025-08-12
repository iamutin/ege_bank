from django.db import models
from django.utils.timezone import now


class Problem(models.Model):
    TASK_TYPE_CHOICES = (
        ("text", "Задача с кратким ответом"),
        ("match", "Установить соответствие"),
    )

    number = models.CharField(max_length=10, unique=True, verbose_name="Номер задачи")
    text = models.TextField(verbose_name="Текст условия")
    illustration = models.ImageField(
        upload_to="illustrations/",
        blank=True,
        null=True,
        verbose_name="Поясняющее изображение",
    )
    task_type = models.CharField(
        max_length=10,
        choices=TASK_TYPE_CHOICES,
        default="text",
        verbose_name="Тип задания",
    )
    answer = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Верный ответ (для краткого ответа)",
        help_text="Заполняется только для задач с типом 'text'",
    )
    unit = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name="Единица измерения",
        help_text="Заполняется только для задач с типом 'text'",
    )
    created_at = models.DateTimeField(
        default=now, editable=False, verbose_name="Время создания"
    )

    def __str__(self):
        return f"Задача №{self.number}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "задача"
        verbose_name_plural = "задачи"


class MatchAnswerOption(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="match_answer_options",
        verbose_name="Задача",
    )
    label = models.CharField(max_length=1, verbose_name="Метка (например, 1, 2, 3, 4)")
    text = models.TextField(verbose_name="Текст варианта")

    class Meta:
        ordering = ["label"]
        unique_together = ("problem", "label")
        verbose_name = "Вариант ответа (справа)"
        verbose_name_plural = "Варианты ответа (справа)"

    def __str__(self):
        return f"{self.problem} — Вариант {self.label}"


class MatchOption(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="match_options",
        verbose_name="Задача",
    )
    label = models.CharField(max_length=1, verbose_name="Метка")
    text = models.TextField(
        blank=True, null=True, verbose_name="Текст формулы или описания"
    )
    image = models.ImageField(
        upload_to="match_options/",
        blank=True,
        null=True,
        verbose_name="Изображение (если есть)",
    )
    correct_answer = models.ForeignKey(
        MatchAnswerOption,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Правильный ответ",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["label"]
        unique_together = ("problem", "label")
        verbose_name = "Соответствие (A или Б)"
        verbose_name_plural = "Соответствия (A и Б)"

    def __str__(self):
        return f"{self.problem} — {self.label}"
