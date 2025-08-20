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


class MatchLeftOption(models.Model):
    """Левая часть (А и Б)"""

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="left_options",
        verbose_name="Задача",
    )
    label = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B")],
        verbose_name="Метка (A или Б)",
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Текст (например, формула или описание)",
    )
    image = models.ImageField(
        upload_to="match_left/",
        blank=True,
        null=True,
        verbose_name="Изображение (если есть)",
    )

    class Meta:
        ordering = ["label"]
        unique_together = ("problem", "label")
        verbose_name = "Элемент слева (А или Б)"
        verbose_name_plural = "Элементы слева (А и Б)"

    def __str__(self):
        return f"{self.label}"


class MatchRightOption(models.Model):
    """Правая часть (варианты 1–4)"""

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="right_options",
        verbose_name="Задача",
    )
    index = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 5)],
        verbose_name="Номер варианта (1–4)",
    )
    text = models.TextField(verbose_name="Текст варианта")

    class Meta:
        ordering = ["index"]
        unique_together = ("problem", "index")
        verbose_name = "Вариант справа (1–4)"
        verbose_name_plural = "Варианты справа (1–4)"

    def __str__(self):
        return f"{self.index}"


class MatchPair(models.Model):
    """Правильная связка: A/Б → 1–4"""

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="pairs",
        verbose_name="Задача",
    )
    left_option = models.OneToOneField(
        MatchLeftOption,
        on_delete=models.CASCADE,
        related_name="pair",
        verbose_name="Элемент слева (A или Б)",
    )
    right_option = models.ForeignKey(
        MatchRightOption,
        on_delete=models.CASCADE,
        related_name="pairs",
        verbose_name="Правильный вариант справа (1–4)",
    )

    class Meta:
        verbose_name = "Соответствие (A → 1)"
        verbose_name_plural = "Соответствия (A → 1)"

    def __str__(self):
        return f"{self.left_option.label} → {self.right_option.index}"
