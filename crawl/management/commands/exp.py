# -*- coding: utf-8 -*


import time

import random
import simplejson as json
from django.core.management.base import BaseCommand
from crawl.models import SocialDetails
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from settings.production import ins_passwords, ins_tags, ins_comments

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):

        descr = [am for am in SocialDetails.objects.filter(details__isnull=False)]
        for i in descr:
            descr_text = json.loads(i.details)

