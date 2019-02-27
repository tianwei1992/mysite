from django import forms
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column", )

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body" )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator", "body")

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag", )

class SearchForm(forms.Form):
    year_choices = (2018, 2019, 2020, 2021)
    choices = [('author', '作者'), ('title','标题'), ('body','内容'), ('all', '不限')]
    by_which = forms.ChoiceField(widget=forms.Select,choices=choices, required=True) 
    keywords = forms.CharField(required=True, max_length=50, strip=True)
    date_st = forms.DateField(widget=forms.SelectDateWidget(years=year_choices))
    date_ed = forms.DateField(widget=forms.SelectDateWidget(years=year_choices))
