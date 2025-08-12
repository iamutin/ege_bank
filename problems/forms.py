from django.forms import BaseInlineFormSet


class MatchAnswerOptionFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        instance = form.save(commit=False)
        # Присваиваем label только новой форме, если он еще не установлен
        if not instance.label:
            instance.label = str(self._labels_assigned)
            self._labels_assigned += 1
        if commit:
            instance.save()
        return instance

    def save_existing(self, form, instance, commit=True):
        # НЕ перезаписываем label у существующих записей
        return super().save_existing(form, instance, commit)

    def save(self, commit=True):
        self._labels_assigned = 1  # Нумерация: "1", "2", "3", "4"
        return super().save(commit)


class MatchOptionFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        instance = form.save(commit=False)
        if not instance.label:
            instance.label = self._next_label()
        if commit:
            instance.save()
        return instance

    def save_existing(self, form, instance, commit=True):
        # НЕ перезаписываем label у существующих записей
        return super().save_existing(form, instance, commit)

    def save(self, commit=True):
        self._label_index = 0
        return super().save(commit)

    def _next_label(self):
        labels = ["А", "Б"]
        label = labels[self._label_index]
        self._label_index += 1
        return label
