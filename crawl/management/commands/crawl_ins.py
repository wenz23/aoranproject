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

        q = Queue()
        existing_list = set([am.url.lower() for am in SocialTracking.objects.filter(social_media_type='Instagram')])
        starting_list = [am.ins_url.lower() for am in ProcessInstagram.objects.all()]
        for i in starting_list:
            if i not in existing_list:
                q.put(i)
        print("Starting Queue Size # ", q.qsize())

        # setting up queue
        sys_threads = threading.active_count()
        threads = 10
        c = 0

        #############################
        # parse_via_q(q)
        #############################

        while not q.empty():
            try:
                c += 1
                tc = threading.active_count()
                if tc < (threads + sys_threads):
                    print('Active Threads::' + str(tc))
                    worker = Thread(target=parse_via_q, args=(q,))
                    worker.daemon = True
                    worker.start()
                    time.sleep(0.1)
                else:
                    time.sleep(150)
            except Exception as e:
                print(e)
