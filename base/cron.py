# django
from django.contrib.sessions.management.commands import clearsessions

# django cron
from django_cron import CronJobBase
from django_cron import CronJobManager
from django_cron import Schedule


class BaseCronJob(CronJobBase):

    @classmethod
    def release(cls):
        silent = False
        with CronJobManager(cls, silent) as manager:
            lock = manager.lock_class(cls, manager.silent)
            lock.release()


class ClearSessionsCronJob(CronJobBase):
    RUN_AT_TIMES = ('03:00',)

    schedule = Schedule(
        run_at_times=RUN_AT_TIMES,
    )
    code = 'base.ClearSessionsCronJob'

    def do(self):
        clearsessions.Command().handle()
