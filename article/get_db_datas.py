import logging
logger = logging.getLogger('mysite.error')
search_logger = logging.getLogger('mysite.article.info')
from .models import ArticleColumn, ArticlePost, Comment, Applaud


def search_articles_by(by_which, keywords, date_st, date_ed):
    """return a querySet of articles """
    if by_which == "all":
        """不限拆成3次查询，结果取交集"""
        by_which_list = ['author', 'title', 'body']
    else:
        by_which_list = [by_which]
    
    articles = []    
    for by_which in by_which_list:
        if by_which == "author":
            by_which = by_which + '__username'
        query_line = 'ArticlePost.objects.filter(' + by_which +'__contains="' + keywords+'", created__range=(date_st, date_ed))'
        search_logger.info(query_line)
        res = eval(query_line)
        articles.extend(list(res))

    if articles:
        search_logger.info("query_set exists:{}".format(len(articles)))
    else:
        search_logger.info("query_set no exists")
        

    return articles
    
