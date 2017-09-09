import time
from datetime import date, timedelta
from django.db.models import Count, Min, Max
import urllib3
from django.core.management.base import BaseCommand

from crawl.crawler import *
from crawl.models import InstagramMap, InstagramTracking

urllib3.disable_warnings()


def fast_growth_users():
    follower_growth = [i for i in InstagramMap.objects.filter(ins_growth__rate__isnull=False)]


    print("Done")


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fast_growth_users()

