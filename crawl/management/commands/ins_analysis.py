import time
from datetime import date, timedelta
from django.db.models import Count, Min, Max
import urllib3
from django.core.management.base import BaseCommand

from crawl.crawler import *
from crawl.models import InstagramMap, InstagramTracking

urllib3.disable_warnings()


def fast_growth_user():
    follower_growth = [i for i in InstagramTracking.objects.values(
        'ins_username', 'created_at', 'ins_follower_count').all().order_by('created_at')]
    username_map = dict()

    for i in follower_growth:
        if i['ins_username'] in username_map:
            username_map[i['ins_username']] += [i['created_at'], i['ins_follower_count']]
        else:
            username_map[i['ins_username']] = [i['created_at'].isoformat() , i['ins_follower_count']]


    print("Done")


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fast_growth_user()

