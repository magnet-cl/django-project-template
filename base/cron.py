# django cron
from django_cron import CronJobBase
from django_cron import CronJobManager


class BaseCronJob(CronJobBase):

    @classmethod
    def release(cls):
        silent = False
        with CronJobManager(cls, silent) as manager:
            lock = manager.lock_class(cls, manager.silent)
            lock.release()
