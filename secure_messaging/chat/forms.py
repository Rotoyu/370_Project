from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a recipient")
    content = forms.CharField(widget=forms.Textarea)
