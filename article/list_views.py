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

from utils.get_client_infos import get_visitor_ip, get_useragent, get_visitor_infos
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


def paginate(item_list, page,  num_per_page=4):
    """分页函数"""
    paginator = Paginator(item_list, num_per_page)

    try:
        current_page = paginator.page(page)
        item_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        item_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        item_list = current_page.object_list
    return current_page, item_list


def update_views_and_ranking(article_id):
    total_views = r.incr("article:{}:views".format(article_id)) # 更新文章访问次数
    r.zincrby("article_ranking", article_id, 1) # 更新文章排名
    return total_views


def article_titles(request, username=None):
    """文章标题页，username指定某位作者的文章标题页，分页显示"""
    if username:
        """指定用户文章标题页"""
        article_titles, author, userinfo = ArticlePost.get_articles_with_userinfo_by_authorname(author_name=username)
    else:
        """公共文章标题页"""
        article_titles = ArticlePost.get_articles_all()

    # 分页
    NUM_OF_ARTICLES_PER_PAGE = 4
    page = request.GET.get("page") or '1'
    current_page, articles = paginate(article_titles, page, NUM_OF_ARTICLES_PER_PAGE, )


    # 提取客户端相关信息
    ip, ip_infos, ua = get_visitor_infos(request)
    visitor = request.user.username if request.user.is_authenticated else "Anomynmous"

    # 记录日志
    if username:
        log_str = '[public visit]author_article_titles'
        start_logging.delay(log_str, ip=ip, username=visitor, ua=ua, Page=page, Author=username)

        context = {
            "articles": articles,
            "page": current_page,
            "userinfo": userinfo,
            "user_to_show": author
        }
        template_path = "article/list/author_articles.html"
    else:
        log_str = '[public visit]article_titles'
        start_logging.delay(log_str,  ip=ip, username=visitor, ua=ua, Page=page)

        context = {
            "articles": articles,
            "page": current_page,
            "search_form": SearchForm()
        }
        template_path = "article/list/article_titles.html"
    return render(request, template_path, context)


def article_detail(request, id, slug):
    ip, ip_infos, ua = get_visitor_infos(request)

    cur_user = request.user if request.user.is_authenticated else None
    username = cur_user.username if cur_user else "Anonymous"
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    article_path = request.get_full_path()

    total_views = update_views_and_ranking(id)
    most_viewed = ArticlePost.get_most_viewed_articles()
    similar_articles = article.get_similar_articles()

    if request.method == "POST":
        if_as_login = request.POST.get("if_as_login")
        body = request.POST.get("body")    # if_login...
        comment_form = CommentForm(data=request.POST)    # else not login...

        if if_as_login:   # if comment as a login user, comments are saved in UserComment
            if cur_user and body:
                article.save_a_usercomment(body, cur_user)
                return HttpResponseRedirect(article_path)
            else:
                return HttpResponse("不允许的操作，未登录或者评论内容为空")
        else:    # comment as a  visitor, comments are saved in Comment
            if comment_form.is_valid():
                article.save_a_visitorcomment(comment_form)
                return HttpResponseRedirect(article_path)
            else:
                info_logger.info("表单无效:{}".format(comment_form.errors))
                return HttpResponse("评论失败，请检查")

    elif request.method == "GET":
        log_str = '[public visit]article_detail'
        start_logging.delay(log_str, ip=ip, username=username, views=str(total_views), title=article.title, )

    comment_form = CommentForm()
    context = {
        "article": article,
        "total_views": total_views,
        "most_viewed": most_viewed,
        "comment_form": comment_form,
        "similar_articles": similar_articles,
        "cur_user": cur_user,
    }
    return render(request, "article/list/article_detail.html", context)


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
