from django import forms
from django.contrib.auth.models import User
from .models import Communication 

class CommunicationForm(forms.ModelForm):

    sender = forms.CharField(label='Sender')
    receiver = forms.CharField(label='Receiver')
    message = forms.CharField(widget=forms.Textarea(attrs={
                    "rows":2,
                    "cols":80,
                    "style":"resize:none;border-color:silver; border-width:1px; border-radius: 5px;",
                    "placeholder": "",
                    }), label='MENSAGEM',)    
    
    class Meta:
        model = Communication
        fields = ('sender', 'receiver', 'message')