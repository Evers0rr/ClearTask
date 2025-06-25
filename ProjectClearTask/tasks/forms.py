from django import forms
from .models import Task,Comments
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дедлайн',
        help_text='Оберіть кінцеву дату виконання завдання.'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        labels = {
            'title': 'Назва завдання',
            'description': 'Опис',
            'status': 'Статус',
            'priority': 'Пріоритет',
        }
        help_texts = {
            'title': 'Вкажіть назву.',
            'description': 'Опишіть деталі вашого завдання.',
            'status': 'Оберіть поточний стан завдання.',
            'priority': 'Оберіть рівень пріоритету.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зберегти'))

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < timezone.now().date():
            raise forms.ValidationError("Дата не може бути в минулому.")
        return due_date
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        labels = {'text': 'Коментар'}
        help_texts = {'text': 'Залиште свій коментар до завдання.'}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Введіть ваш коментар тут...',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Надіслати'))