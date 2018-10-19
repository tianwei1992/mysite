from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_POST

def article_titles(request, username=None):
    if username:
        user =  User.objects.get(username=username)
        article_titles = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_titles = ArticlePost.objects.all()
    paginator = Paginator(article_titles, 2)
    page = request.GET.get("page")
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html",{ "articles":articles, "page":current_page, "userinfo":userinfo, "user":user})
    else:
        return render(request, "article/list/article_titles.html", {"articles":articles, "page":current_page})

def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/list/article_detail.html", {"article": article})

@require_POST
def like_article(request):
    if request.user.is_authenticated:
        article_id = request.POST.get("id")
        action = request.POST.get("action")
        if article_id and action:
            try:
                article = ArticlePost.objects.get(id=article_id)
                if action == "like":
                    article.users_like.add(request.user)
                    return HttpResponse("1")
                else:
                    article.users_like.remove(request.user)
                    return HttpResponse("2")
            except Exception as e:
                print(e)
                return HttpResponse("no")
    else:
        return HttpResponse('/account/new-login/?next=%s' % request.path)
