import traceback
import logging
logger = logging.getLogger('mysite.error')

import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm

# Create your views here.
@login_required(login_url='/account/login/')
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form}) 
    elif request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@require_POST
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except Exception as e:
        logger.error(traceback.print_exc())
        return HttpResponse("0")


@login_required(login_url='/account/login/')
@require_POST
def delete_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id, user=request.user)
        line.delete()
        return HttpResponse("1")
    except ArticleColumn.DoesNotExist as e:
        logger.error("Attack? delete_article_column column_id={}, author={}".format(column_id, request.user))
        return HttpResponse("0")
    except Exception as e:
        logger.error(traceback.print_exc())
        return HttpResponse("0")

@login_required(login_url='/account/login/')
def article_post(request):
    if request.method == "POST":
        articlepost_form = ArticlePostForm(request.POST)
        if articlepost_form.is_valid():
            cd = articlepost_form.cleaned_data
            try:
                new_article = articlepost_form.save(commit=False)            
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST["column_id"]) 
                new_article.save()
                # save article tag as well
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        tag.article_tag.add(new_article)
                        # todo:ok?
                        # new_article.article_tag.add(tag)
                return HttpResponse("1")
            except Exception as e:
                logger.error(traceback.print_exc())
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    elif request.method == "GET":
        articlepost_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html", {"article_columns":article_columns, "articlepost_form":articlepost_form, "article_tags": article_tags})

@login_required(login_url='/account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles":articles, "page": current_page})

@login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, author=request.user, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article":article})


@login_required(login_url='/account/login/')
@require_POST
def delete_article(request):
    article_id = request.POST["article_id"]
    try:
        line = ArticlePost.objects.get(id=article_id, author=request.user)
        line.delete()
        return HttpResponse("1")
    except ArticlePost.DoesNotExist as e:
        logger.error("Attack? delete_article article_id={}, author={}".format(article_id, request.user))
        return HttpResponse("0")
    except Exception as e:
        logger.error(traceback.print_exc())
        return HttpResponse("0")

@login_required(login_url='/account/login/')
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html", {"article":article, "article_columns": article_columns, "this_article_form":this_article_form, "this_article_column": this_article_column})
    elif request.method == "POST":
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except: 
            return HttpResponse("0")


@login_required(login_url='/account/login/')
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags": article_tags, "article_tag_form": article_tag_form})
    elif request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                logger.error(traceback.print_exc())
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry, the form is not valid")


@login_required(login_url='/account/login/')
@require_POST
def delete_article_tag(request):
    tag_id = request.POST["tag_id"]
    try:
        line = ArticleTag.objects.get(id=tag_id, author=request.user)
        line.delete()
        return HttpResponse("1")
    except ArticleTag.DoesNotExist as e:
        logger.error("Attack? delete_article_tag tag_id={}, author={}".format(tag_id, request.user))
        return HttpResponse("2")
    except Exception as e:
        logger.error(traceback.print_exc())
        return HttpResponse("2")
