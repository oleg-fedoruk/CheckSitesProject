from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import datetime


class Site(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название компании')
    site_url = models.URLField(max_length=50, verbose_name='Сайт')
    is_active = models.BooleanField(verbose_name='Проверять')
    responsible_users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sites'
        ordering = ['-is_active']

    def get_absolute_url(self):
        return reverse('site_view', args=[str(self.id)])


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status_code = models.CharField(max_length=300)
    the_site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return datetime.strftime(self.created_at, '%Y-%m-%d %H:%M')

    class Meta:
        ordering = ['the_site']
