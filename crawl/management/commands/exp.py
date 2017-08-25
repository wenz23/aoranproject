from django.core.management.base import BaseCommand

from crawl.crawler import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        req_content = lambda_crawler_request(username="zerkaahd", social_type="ins")
        if req_content:
            # Parse
            ins_tracking_obj = crawl_ins_username_via_lambda(req_content=req_content)
            try:
                ins_tracking_obj.save()
            except Exception as e:
                print(e)
            print("Done")


