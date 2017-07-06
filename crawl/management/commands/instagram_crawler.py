import urllib3
from aoranproject.common import ins_lambda_request
from django.core.management.base import BaseCommand

urllib3.disable_warnings()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(ins_lambda_request(usr='a.wen.z', use_proxy=False))
