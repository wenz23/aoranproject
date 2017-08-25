import threading
import time
from queue import Queue
from threading import Thread
from crawl.crawler import *

import urllib3
from django.core.management.base import BaseCommand


urllib3.disable_warnings()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        activate_ins_crawl()