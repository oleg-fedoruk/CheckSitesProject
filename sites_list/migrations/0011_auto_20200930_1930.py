# Generated by Django 2.2 on 2020-09-30 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites_list', '0010_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='responsible_users',
            field=models.ManyToManyField(to='sites_list.Profile'),
        ),
    ]
