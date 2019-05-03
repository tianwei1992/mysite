## 启动步骤
1. 先启动Django
2. 再启动Celery Worker(在mysite目录下)
```
celery multi start w1 -A mysite -l info
```
3. 还要启动Redis
```
/opt/redis-5.0.0/src# ./redis-server ../redis60025.conf
```
## 2019.05.03 重构视图函数
### 重构article.list_views.article_titles & article.list_views.article_detail
1. 提取在views的公共部分:paginate()和update_views_and_ranking()
2. 提取在models.ArticlePost的公共部分：get_articles_with_userinfo_by_authorname(), get_most_viewed_articles()等
3. article_detail中的日志部分改为celery异步，记得启动celery
4. 获取ip、ip_info、ua进一步集中提取到一个函数get_visitor_info