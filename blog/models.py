from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogArticles(models.Model):
    """数据模型类，这是数据库表结构的基础"""
    # 第1个字段
    title = models.CharField(max_length=300)
    # author- > blog_posts, i.e. one to multiple
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    # 第3个字段
    body = models.TextField()
    # 第4个字段
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)
    
    def __str__(self):
        # 指定BlogArticles实例对象名
        return self.title
