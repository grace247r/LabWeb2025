from django import forms
from .models import DRFPost

class DRFPostForm(forms.ModelForm):
    class Meta:
        model = DRFPost
        fields = '__all__'