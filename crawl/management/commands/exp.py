
import re
import requests
from django.utils import timezone
from crawl.models import InstagramMap
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        map_objs = [am for am in InstagramMap.objects.exclude(project_info={})]
        for i in map_objs:
            i.project_info = {'p': 'Fashion'}
            i.save()
            print("Done")