from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models import Count
from django.utils.functional import cached_property

import redis

from slugify import slugify

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)


# Create your models here.
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name="article_column", on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag", on_delete=models.CASCADE)
    tag = models.CharField(max_length=500)
    
    def __str__(self):
        return self.tag

class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name="article_column", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name="article_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name="article_tag", blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        REPLACE_CHAPTER = '-'
        self.slug = slugify(self.title)
        if not self.slug:     # To deal with: slugify('-') == "" 
            self.slug = REPLACE_CHAPTER 
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        # print(reverse("article:article_detail", args=[self.id, self.slug]))
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        # print(reverse("article:article_detail", args=[self.id, self.slug]))
        return reverse("article:list_article_detail", args=[self.id, self.slug])

    @classmethod
    def get_articles_with_userinfo_by_authorname(cls, author_name):
        userinfo = None
        try:
            author = User.objects.get(username=author_name)
            userinfo = author.userinfo
            article_titles = cls.objects.filter(author=author)
        except User.DoesNotExist:
            author = None
            article_titles = cls.objects.none()

        return article_titles, author, userinfo

    @classmethod
    def get_articles_all(cls):
        article_titles = ArticlePost.objects.select_related('author').all()
        return article_titles

    @classmethod
    def get_most_viewed_articles(cls):
        article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
        article_ranking_ids = [int(id) for id in article_ranking]
        most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
        most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
        return most_viewed

    def get_similar_articles(self):
        article_tags = self.article_tag.all()  # #从一个tag获得对应的所有Aricle对象
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags).exclude(id=self.id)
        similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[
                           :4]
        return similar_articles

    def save_a_usercomment(self, body, user):
        new_comment = UserComment()
        new_comment.article = self
        new_comment.body = body
        new_comment.commentator = user
        new_comment.save()

    def save_a_visitorcomment(self, comment_form):
        new_comment = comment_form.save(commit=False)
        new_comment.article = self
        new_comment.save()

    @cached_property
    def tags(self):
        return ','.join(self.article_tag.values_list('tag', flat=True))



class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comments", on_delete="CASCADE")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)


class UserComment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="user_comments", on_delete="CASCADE")
    commentator= models.ForeignKey(User, related_name="user_comments", on_delete="CASCADE")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)


class Applaud(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="applauds", on_delete="CASCADE")
    applauder = models.ForeignKey(User, related_name="applauds", on_delete="CASCADE")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together=("article","applauder")

    def __str__(self):
        return "Applaud by {0} on {1}".format(self.applauder.username, self.article)

    def save(self, *args, **kargs):
        try:    # applaud twice or more will affect nothing
            super(Applaud, self).save(*args, **kargs)
        except IntegrityError:
            pass
