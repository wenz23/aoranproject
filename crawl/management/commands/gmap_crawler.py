# -*- coding: utf-8 -*


import time

import random
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from settings.production import ins_passwords, ins_tags, ins_comments


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        pass

