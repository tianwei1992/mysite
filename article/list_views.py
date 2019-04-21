import sys
import os
import json
import traceback
import logging

import redis

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Count

from utils.get_client_infos import get_visitor_ip, get_useragent
from utils.get_ip_infos import get_location_calling_free_api
from utils.get_client_infos import get_visitor_ip, get_useragent
from utils.get_ip_infos import get_location_calling_free_api

from .models import ArticleColumn, ArticlePost, Comment, UserComment, Applaud
from .forms import CommentForm, SearchForm
from .tasks import start_logging
from .get_db_datas import search_articles_by

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

logger = logging.getLogger('mysite.error')
info_logger = logging.getLogger('mysite.article.info')
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)


def article_titles(request, username=None):
    """文章标题页，username指定某位作者的文章标题页，分页显示"""
    if username:
        """公共文章标题页"""
        user =  User.objects.get(username=username)
        article_titles = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        """指定用户文章标题页"""
        article_titles = ArticlePost.objects.all()

   # 分页 
    paginator = Paginator(article_titles, 2)
    page = request.GET.get("page") or '1'
    try:

        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    # 提取客户端相关信息
    ip = get_visitor_ip(request)
    ua = get_useragent(request)
    visitor = request.user.username if request.user.is_authenticated else "Anomynmous"
    
    # 开始记录日志
    if username:
        log_str = '[public visit]author_article_titles'
        start_logging.delay(log_str, ip=ip, username=visitor, ua=ua, Page=page, Author=username) 
        # info_logger.info('[public visit]auhor_article_titles ip:{}[{}] author:{} page:{}'.format(ip, ip_infos, request.user.username, current_page))
        return render(request, "article/list/author_articles.html",{ "articles":articles, "page":current_page, "userinfo":userinfo, "user_to_show":user})
    else:
        log_str = '[public visit]article_titles'
        start_logging.delay(log_str,  ip=ip, username=visitor, ua=ua, Page=page) 
        # info_logger.info('[public visit]article_titles ip:{}[{}] visitor:{} page:{} ua:{}'.format(ip, ip_infos,  request.user.username if request.user.is_authenticated else "Anonymous", current_page, ua))
        search_form = SearchForm()
        return render(request, "article/list/article_titles.html", {"articles":articles, "page":current_page,"search_form": search_form})


def article_detail(request, id, slug):
    ip = get_visitor_ip(request)
    ip_infos = get_location_calling_free_api(ip)
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
        if request.POST.get("if_as_login"):
        # if comment as a login user, comments are saved in UserComment
            body = request.POST.get("body")
            if request.user.is_authenticated and body:   
                new_comment = UserComment()
                new_comment.article = article
                new_comment.body = body
                new_comment.commentator = request.user
                new_comment.save()

                article_path = request.get_full_path()
                return HttpResponseRedirect(article_path)
            else:
                return HttpResponse(" Not Allowd, login first,please")
        else:
        # comment as a  visitor, comments are saved in Comment
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.save()

                article_path = request.get_full_path()
                return HttpResponseRedirect(article_path)
            else:
                info_logger.info("表单无效:{}".format(comment_form.errors))
                return HttpResponse("评论失败，请检查")
                # logger.error(traceback.print_exc())
    elif request.method == "GET":
        info_logger.info('[public visit]article_detail ip:{}[{}] visitor:{} title:{} views:{}'.format(ip, ip_infos, request.user.username if request.user.is_authenticated else "Anonymous", article.title, total_views))

    # starting to return...
    cur_user = None
    if request.user.is_authenticated:
        cur_user = request.user 
    comment_form = CommentForm()

    return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views, "most_viewed": most_viewed, "comment_form":comment_form, "similar_articles": similar_articles, "cur_user": cur_user})


@require_POST
def like_article(request):
    if request.user.is_authenticated:
        article_id = request.POST.get("id")
        action = request.POST.get("action")
        if article_id and action:
            try:
                article = ArticlePost.objects.get(id=article_id)
                if action == "like":
                    info_logger.info('like {} {}'.format(article_id, action))
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
                # logger.error(traceback.print_exc())
                return HttpResponse("no")
    else:
        article_path = request.POST.get("article_url")
        return HttpResponse('/account/new-login/?next=%s' % article_path)


@require_POST
def article_search(request, username=None):
    ip = get_visitor_ip(request)
    ip_infos = get_location_calling_free_api(ip)
    ua = get_useragent(request)
    search_form = SearchForm(data=request.POST)
    articles_list = []
    if search_form.is_valid():
        flg = 1
        cd = search_form.cleaned_data
        if cd:
            by_which = cd['by_which']
            keywords = cd['keywords']
            date_st = cd['date_st']
            date_ed = cd['date_ed']
        # get a query_set by k
        articles_list = search_articles_by(by_which, keywords, date_st, date_ed);
    else:
        flg = 0
    res = {"status": flg}
    article_info_list = [(article.title, article.author.username, article.author.username, article.get_url_path(), article.body[:80]) for article in articles_list]
    res.update({"articles": article_info_list})
    return HttpResponse(json.dumps(res))
