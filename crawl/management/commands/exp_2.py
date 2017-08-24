from aoranproject.common import api_gateway, lambda_crawler_request
from django.core.management.base import BaseCommand
import datetime
from json import loads
from crawl.models import SocialTracking, ProcessInstagram


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        ins_list = list(set([am.url for am in SocialTracking.objects.filter(social_media_type='Instagram',
                                                                            ins_follower_count__gt=3000)]))

        for i in ins_list:
            obj, created = ProcessInstagram.objects.get_or_create(ins_url=i.lower())

