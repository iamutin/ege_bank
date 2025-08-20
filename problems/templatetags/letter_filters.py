from django import template

register = template.Library()

LATIN_TO_CYRILLIC = {
    "A": "А",
    "B": "Б",
    "C": "В",
    "D": "Г",
}

@register.filter
def cyrillic(value: str) -> str:
    """Преобразует латинские буквы A, B, C, D в кириллические А, Б, В, Г"""
    if not value:
        return ""
    return LATIN_TO_CYRILLIC.get(value, value)
