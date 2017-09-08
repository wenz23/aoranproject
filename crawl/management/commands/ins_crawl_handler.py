import time
from datetime import date, timedelta

import urllib3
from django.core.management.base import BaseCommand

from crawl.crawler import *
from crawl.models import InstagramMap

urllib3.disable_warnings()


def activate_ins_crawl():

    prior_week = date.today() - timedelta(7)
    # ins_to_crawl_list = [am for am in InstagramMap.objects.filter(
    #     Q(latest_crawl_state__in=[StateEnum.Parse_Failed, StateEnum.Req_Failed, StateEnum.New, StateEnum.Standby, StateEnum.Req_Success]) |
    #     Q(latest_crawl_state=StateEnum.Parse_Success, latest_crawl_at__gte=prior_week))]

    ins_to_crawl_list = [am for am in InstagramMap.objects.exclude(latest_crawl_state__in=[600, 404]).order_by('-created_at')]
    # ins_to_crawl_list = [am for am in
    #                      InstagramMap.objects.exclude(latest_crawl_state__in=[404]).order_by('-created_at')]

    print("Start: ", len(ins_to_crawl_list))
    counter = 0
    for ins_map_obj in ins_to_crawl_list:
        time.sleep(0.5)
        counter += 1
        if counter % 100 == 0:
            print(len(ins_to_crawl_list)-counter, " TO GO")
        req_content = lambda_crawler_request(username=ins_map_obj.latest_username)
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
                ins_map_obj.save()

            except Exception as e:
                print("Parse Failed. Username: ", str(ins_map_obj.latest_username), ". Because: ", str(e))
                ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                ins_map_obj.save()

        else:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Failed
            ins_map_obj.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        activate_ins_crawl()

