from django.db import models
from django.urls import reverse


class Site(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название компании')
    site = models.URLField(max_length=50, verbose_name='Сайт')
    is_active = models.BooleanField(verbose_name='Проверять')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sites'
        ordering = ['-is_active']

    def get_absolute_url(self):
        return reverse('site_view', args=[str(self.id)])
