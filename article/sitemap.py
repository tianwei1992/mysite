from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import ArticlePost


class ArticlePostSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ArticlePost.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse('article:list_article_detail', args=[obj.pk, obj.slug])
