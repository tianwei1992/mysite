# Generated by Django 2.1.2 on 2018-12-08 08:38

import course.fields
import course.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('vedio', models.FileField(upload_to=course.models.user_directory_path)),
                ('attach', models.FileField(upload_to=course.models.user_directory_path)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('order', course.fields.OrderField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete='CASCADE', related_name='lesson', to='course.Course')),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='lesson_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
