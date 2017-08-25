import threading
import time
from queue import Queue
from threading import Thread

import urllib3
from django.core.management.base import BaseCommand

from crawl.models import SocialTracking, ProcessInstagram

urllib3.disable_warnings()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pass