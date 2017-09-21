import threading
import time
from queue import Queue

import urllib3
from django.core.management.base import BaseCommand
from simplejson import loads

from crawl.crawler import lambda_crawler_request
from crawl.models import InstagramMap

urllib3.disable_warnings()


def build_a_queue():
    q = Queue()
    ins_to_crawl_list_exp = [am.latest_username for am in InstagramMap.objects.exclude(latest_crawl_state__in=[404])[:22]]
    for i in ins_to_crawl_list_exp:
        q.put(i)

    print("Queue Size: ", q.qsize())
    return q


def lambda_crawler_request_wrapper(q):
    while not q.empty():
        q_name  = q.get()
        req_content = lambda_crawler_request(username=q_name)
        try:
            dictionary = loads(req_content)
            username = dictionary['entry_data']['ProfilePage'][0]['user']['username']
            print('Success ', 'Queue Size ', q.qsize(), username)
        except:
            print('Error ', q_name)
    return True


def thread_wrapper_for_q(thread_count=1, c_function=None, q=None, lock_main_thread=True):
    worker = None
    if c_function and q:
        print("====================")
        print("Qsize count:")
        print(q.qsize())
        print("====================")
        for i in range(thread_count):
            if not q.empty():
                worker = threading.Thread(target=c_function, args=(q,))
                worker.daemon = False
                worker.start()
                time.sleep(0.1)
            else:
                return True
        if lock_main_thread and worker:
            worker.join()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        queue = build_a_queue()

        thread_wrapper_for_q(thread_count=20, c_function=lambda_crawler_request_wrapper, q=queue)
