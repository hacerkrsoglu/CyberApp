from django import forms
from django_ckeditor_5.fields import CKEditor5Field
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
  
    content=CKEditor5Field('Text', config_name='default')

    class Meta:
        model = Message
        fields = ['subject', 'content']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.receiver = User.objects.get(username='hacer')  # Receiver'ı burada ayarladım
        if commit:
            instance.save()
        return instance
