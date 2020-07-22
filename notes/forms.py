from .models import NoteBoard
from django.forms import ModelForm, TextInput, Textarea


class TaskForm(ModelForm):
    class Meta:
        model = NoteBoard
        fields = ["note_title", "note_text", "note_tags"]
        widgets = {
            "note_title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': r'Название',
                'maxlength': 100

            }),
            "note_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': r'Заметка',
                'maxlength': 3000
            }),
            "note_tags": TextInput(attrs={
                'class': 'form-control',
                'placeholder': r'Тэги',
                'maxlength': 30
            }),
        }

