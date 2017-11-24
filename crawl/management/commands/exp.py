import numpy as np
import pandas as pd
import json
import requests
from crawl.models import InstagramTracking
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        city = ['seattle', 'hawaii', 'pacific northwest', 'pacific north west', 'university of washington', 'capitol hill', 'uw']
        tag = ['food', 'cooking', 'lifestyle', 'community', 'photography', 'events', 'party',
               'fashion', 'culture', 'media', 'Capitol Hill', 'drinking', 'cocktail', 'clubbing',
               'dining', 'interior', 'travel', 'beach', 'surfing', 'vacation', 'events', 'honeymoon']
        result_objs = []

        for each_city in city:
            for each_tag in tag:
                result_objs += [[am.id, am.ins_username, am.ins_fullname, am.ins_follower_count, am.ins_media_count, am.ins_biography, am.ins_verified, am.ins_external_url, '', ''] for am in InstagramTracking.objects.filter(ins_biography__icontains=each_city).filter(ins_biography__icontains=each_tag)]

        for each_obj in result_objs:
            for each_city in city:
                if each_city in each_obj[5].lower():
                    each_obj[-1] += each_city
                    each_obj[-1] += '; '
            for each_tag in tag:
                if each_tag in each_obj[5].lower():
                    each_obj[-2] += each_tag
                    each_obj[-2] += '; '



        df = pd.DataFrame(result_objs)
        df.to_excel('Done.xlsx', index=False)

