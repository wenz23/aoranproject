import threading
import time
from queue import Queue
from threading import Thread
from crawl.crawler import *

import urllib3
from django.core.management.base import BaseCommand


urllib3.disable_warnings()


def parse_via_q(q):
    while not q.empty():
        ins_map_obj = q.get()
        user_name = str(ins_map_obj.latest_username).lower().strip()
        req_content = lambda_crawler_request(username=user_name, social_type="ins")
        if req_content:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Success
            ins_map_obj.save()

            # Parse
            try:
                result = crawl_ins_username_via_lambda(req_content=req_content, ins_map_obj=ins_map_obj)
                if not result:
                    ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                    ins_map_obj.save()
            except Exception as e:
                print("Parse Failed because: ", str(e))
                ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                ins_map_obj.save()

        else:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Failed
            ins_map_obj.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        q = Queue()
        ins_to_crawl_list = [am for am in InstagramMap.objects.all().order_by('-created_at')]
        for i in ins_to_crawl_list:
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

