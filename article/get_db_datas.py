import logging
logger = logging.getLogger('mysite.error')
search_logger = logging.getLogger('mysite.article.info')
from .models import ArticleColumn, ArticlePost, Comment, Applaud


def search_articles_by(by_which, keywords, date_st, date_ed):
    """return a querySet of articles """
    if by_which == "author":
        by_which = by_which + '__username'
    query_line = 'ArticlePost.objects.filter(' + by_which +'__contains="' + keywords+'", created__range=(date_st, date_ed))'
    search_logger.info(query_line)
    articles = eval(query_line)

    if articles:
        search_logger.info("query_set exists:{}".format(len(articles)))
    else:
        search_logger.info("query_set no exists")
        
    search_logger.info(query_line)
    # search_logger.info('articles = ArticlePost.objects.filter(' + by_which +'__username__contains="' + keywords+'")')

    return list(articles)
    
