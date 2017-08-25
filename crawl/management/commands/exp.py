from aoranproject.common import api_gateway, lambda_crawler_request
from django.core.management.base import BaseCommand
import datetime
from json import loads
from crawl.models import InstagramMap, InstagramTracking


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        objs = [am for am in InstagramTracking.objects.filter(ins_follower_count__gt=2000)]
        for i in objs:
            ins_id = i.ins_id
            ins_username = i.ins_username
            follower = i.ins_follower_count
            map_obj, created = InstagramMap.objects.get_or_create(ins_id=ins_id,
                                                                  defaults={'latest_username': ins_username,
                                                                            'latest_follower_count': follower})
            if not created:
                print('exist:', ins_username)



