# Generated by Django 2.1.2 on 2018-12-08 12:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20181208_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 8, 12, 52, 48, 340687, tzinfo=utc)),
        ),
    ]