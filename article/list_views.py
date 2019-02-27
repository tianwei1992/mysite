import json
import traceback
import logging
logger = logging.getLogger('mysite.error')
info_logger = logging.getLogger('mysite.article.info')
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost, Comment, Applaud
from .forms import CommentForm, SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import redis
from django.conf import settings
from django.db.models import Count
from .get_db_datas import search_articles_by

import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils.get_client_infos import get_visitor_ip, get_useragent

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)

def article_titles(request, username=None):
    ip = get_visitor_ip(request)
    ua = get_useragent(request)
    search_form = SearchForm()
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
        info_logger.info('[public visit]auhor_article_titles ip:{} author:{} page:{}'.format(ip, request.user.username, current_page))
        return render(request, "article/list/author_articles.html",{ "articles":articles, "page":current_page, "userinfo":userinfo, "user_to_show":user})
    else:
        info_logger.info('[public visit]article_titles ip:{} visitor:{} page:{} ua:{}'.format(ip, request.user.username if request.user.is_authenticated else "Anonymous", current_page, ua))
        return render(request, "article/list/article_titles.html", {"articles":articles, "page":current_page,"search_form": search_form})

def article_detail(request, id, slug):
    ip = get_visitor_ip(request)
    ua = get_useragent(request)

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
        info_logger.info('[public visit]article_detail ip:{} visitor:{} title:{} views:{}'.format(ip, request.user.username if request.user.is_authenticated else "Anonymous", article.title, total_views))
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
                    # save it to a new Applaud() including created_time
                    new_applaud = Applaud()
                    new_applaud.applauder = request.user
                    new_applaud.article = article
                    new_applaud.save()
                    return HttpResponse("1")
                else:
                    article.users_like.remove(request.user)
                    # remove it from Applaud model
                    applaud = Applaud.objects.filter(applauder=request.user, article=article)
                    if applaud:
                        applaud.delete()
                    return HttpResponse("2")
            except Exception as e:
                logger.error(traceback.print_exc())
                return HttpResponse("no")
    else:
        article_path = request.POST.get("article_url")
        return HttpResponse('/account/new-login/?next=%s' % article_path)

@require_POST
def article_search(request, username=None):
    ip = get_visitor_ip(request)
    ua = get_useragent(request)
    search_form = SearchForm(data=request.POST)
    articles_list = []
    if search_form.is_valid():
        cd = search_form.cleaned_data
        if cd:
            by_which = cd['by_which']
            keywords = cd['keywords']
            date_st = cd['date_st']
            date_ed = cd['date_ed']
        # get a query_set by k
        articles_list = search_articles_by(by_which, keywords, date_st, date_ed);
        if articles_list:
            flg = 1
        else:
            flg = 2
    else:
        flg = 0
    res = {"status": flg}
    article_info_list = [(article.title, article.author.username, article.body[:80]) for article in articles_list]
    res.update({"articles": article_info_list})
    return HttpResponse(json.dumps(res))

        
             
