import requests
import logging
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_sites_project.settings')
application = get_wsgi_application()


from sites_list.models import Site


log = logging.getLogger('requests_status')
log.setLevel(logging.INFO)
fh = logging.FileHandler('requests_status.log', 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


def get_sites_status():
    all_sites = Site.objects.filter(is_active=True)
    for site in all_sites:
        if site.is_active:
            try:
                url = requests.get(site.site)
                log.info(f'{site.site}, {url.status_code}')
            except:
                log.critical(f'{site.site}, error')


if __name__ == '__main__':
    get_sites_status()
