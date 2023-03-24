from .models import SecretWord
from django import forms


class PasswordForm(forms.ModelForm):
    class Meta:
        model = SecretWord
        fields = ['name', 'url', 'pass_word']
        widgets = {
            'pass_word': forms.PasswordInput(),
        }


