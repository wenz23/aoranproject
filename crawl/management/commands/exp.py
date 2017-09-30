
import re
import requests
from crawl.models import InstagramMap
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        map_objs = [am for am in InstagramMap.objects.all()]
        for i in map_objs:
            i.project_info = {}
            i.save()
            print(i.project_info)
            print(type(i.project_info))
