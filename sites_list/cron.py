from django_cron import CronJobBase, Schedule
from .services import get_sites_status


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'sites_list.cron.MyCronJob'

    def do(self):
        get_sites_status()
