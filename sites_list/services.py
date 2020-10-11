from decimal import Decimal

import requests
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_sites_project.settings')
application = get_wsgi_application()

from sites_list.models import Site, Log
from datetime import datetime, timedelta
from django.core.mail import send_mail


def get_sites_status():  # функция отправляющая запросы к сайтам внесённым в базу данных
    all_sites = Site.objects.filter(is_active=True)
    for site in all_sites:
        try:
            url = requests.get(site.site_url)
            log = Log(status_code=url.status_code, the_site=site)
            log.save()
        except:
            log = Log(status_code='unknown_error', the_site=site)
            log.save()


'''функции для расчёта uptime сайтов'''


def convert_timedelta_in_min(time_delta):  # подсчёт минут из timedelta
    seconds_to_minutes = time_delta.seconds // 60
    days_to_minutes = time_delta.days * 24 * 60
    minutes_sum = seconds_to_minutes + days_to_minutes
    return minutes_sum


def minutes_amount_from_start_of_month():  # определение количества минут, прошедших от начала месяца
    now = datetime.now()
    year, month = now.year, now.month
    first_day_of_month = datetime(year=year, month=month, day=1)
    lost_time_of_month = now - first_day_of_month
    minutes = convert_timedelta_in_min(lost_time_of_month)
    return minutes


def get_status_ok_quantity_logs(site_obj):  # подсчитываем количество записей со
    # статусом 200 у конкретного сайта
    ok_logs_quantity = Log.objects.filter(the_site=site_obj, status_code='200').count()
    return ok_logs_quantity


def get_uptime_percent(site_obj):  # высчитываем процент количества времени
    # успешной работы сайта от начала месяца
    # ВАЖНО: формула высчитывает корректно процентаж, при условии, что запросы на статус работы сайта
    # высылаются с начала месяца без сбоев каждую минуту
    minutes = minutes_amount_from_start_of_month()
    ok_logs_quantity = get_status_ok_quantity_logs(site_obj)
    uptime_percent = (Decimal(ok_logs_quantity / minutes * 100)).quantize(Decimal('1.000'))
    return uptime_percent


'''функции отправки писем с отчётами о работе сайта '''


def send_email_if_error_detected():  # проверка базы данных на наличие сбоев в работе сайтов за последний час
    all_sites = Site.objects.all()

    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)  # определяем временной промежуток длиною в час от настоящего момента

    for site in all_sites:
        # ищем логи, отличающиеся от статуса "200"
        site_logs = Log.objects.filter(the_site=site,
                                       created_at__range=(one_hour_ago, now)
                                       ).exclude(status_code='200')
        if site_logs:  # при нахождении таковых, отправляем уведомления, прикреплённым к сайту юзерам
            users_to_send_mail = site.responsible_users.all()
            for user in users_to_send_mail:
                send_mail(
                    f'Отчёт о работе сайта {site.title}',
                    'Here is the message.',
                    'oleg.fedoruk91@gmail.com',
                    [user.email],
                    fail_silently=False,
                )


if __name__ == '__main__':
    get_sites_status()
