import threading
import time
from queue import Queue

import urllib3
from django.core.management.base import BaseCommand
from django.utils import timezone

from crawl.crawler import lambda_crawler_request, crawl_ins_username_via_lambda, thread_wrapper_for_q
from crawl.models import InstagramMap, StateEnum

urllib3.disable_warnings()


def build_a_queue():
    q = Queue()

    week = timezone.now() - timezone.timedelta(days=5)

    list_1 = [i for i in InstagramMap.objects.exclude(latest_crawl_state__in=[404]).filter(latest_crawl_at__lt=week)]
    list_2 = [i for i in InstagramMap.objects.filter(latest_crawl_at__isnull=True)]

    ins_to_crawl_list = list(set(list_1 + list_2))

    for j in ins_to_crawl_list:
        q.put(j)

    print("Queue Size: ", q.qsize())
    return q


def lambda_crawler_request_wrapper(q):
    while not q.empty():
        ins_map_obj     = q.get()
        req_content     = lambda_crawler_request(username=ins_map_obj.latest_username)

        if req_content:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Success
            ins_map_obj.save()
            # Parse
            try:
                result = crawl_ins_username_via_lambda(req_content=req_content, ins_map_obj=ins_map_obj)

                if not result:
                    ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                elif result == "404":
                    ins_map_obj.latest_crawl_state = StateEnum.User_Not_Exist
                elif result == "Success":
                    ins_map_obj.latest_crawl_state = StateEnum.Parse_Success
                else:
                    ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                ins_map_obj.latest_crawl_at = timezone.now()
                ins_map_obj.save()
                print("Done; ", ins_map_obj.latest_username)
            except Exception as e:
                print("Parse Failed. Username: ", str(ins_map_obj.latest_username), "; Reason: ", str(e))
                ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                ins_map_obj.save()
        else:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Failed
            ins_map_obj.save()
    return True


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        queue = build_a_queue()

        thread_wrapper_for_q(thread_count=4, c_function=lambda_crawler_request_wrapper, q=queue, wait_time=12)
