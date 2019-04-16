from django.contrib import admin

from .models import ArticleColumn 


# Register your models here.
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('user', 'column', 'created')
    list_filter = ("user",)


admin.site.register(ArticleColumn, ArticleColumnAdmin)
