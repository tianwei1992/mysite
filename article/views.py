from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn

# Create your views here.
def article_column(request):
    columns = ArticleColumn.objects.filter(user=request.user)
    return render(request, "article/column/article_column.html", {"columns": columns})

