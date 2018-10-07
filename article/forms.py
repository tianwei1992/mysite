from django import forms
from .models import ArticalColumn

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fillds = ("column", )
