# Generated by Django 2.1.2 on 2018-10-22 14:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20181022_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 14, 19, 15, 838756, tzinfo=utc)),
        ),
    ]