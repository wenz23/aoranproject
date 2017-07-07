from aoranproject.common import api_gateway, lambda_crawler_request
from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        start_time = datetime.datetime.now()
        print(lambda_crawler_request(username="a.wen.z", use_proxy="False", social_type="ins"))
        print(datetime.datetime.now() - start_time)
