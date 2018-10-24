import traceback
import logging
logger = logging.getLogger('mysite.error')
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import redis
from django.conf import settings
from django.db.models import Count

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby("article_ranking", article.id, 1)

    article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    # find out similar articles
    article_tags = article.article_tag.all() # #从一个tag获得对应的所有Aricle对象
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
        else:
            logger.error(traceback.print_exc())
    elif request.method == "GET":
        comment_form = CommentForm()
    return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views, "most_viewed": most_viewed, "comment_form":comment_form, "similar_articles": similar_articles})

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
                logger.error(traceback.print_exc())
                return HttpResponse("no")
    else:
        return HttpResponse('/account/new-login/?next=%s' % request.path)
