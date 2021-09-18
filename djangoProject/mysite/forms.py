from django.forms import ModelForm, widgets
from .models import Title
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Title
        fields = ['title', 'author', 'body_text','date','image']

        widgets ={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'bodytext': forms.Textarea(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),

            
        }

      

