# Generated by Django 2.2 on 2020-09-30 12:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites_list', '0008_auto_20200927_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='responsible_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
