
import re
import requests
from django.utils import timezone
from crawl.models import InstagramMap
from crawl.crawler import lambda_crawler_request
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        content = lambda_crawler_request("ranaoyang")
        print("Done")
