import numpy as np
import pandas as pd
import json
import requests
from crawl.models import InstagramTracking
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        city = ['seattle', 'hawaii', 'pacific northwest', 'pacific north west']
        tag = ['food', 'cooking', 'lifestyle', 'community', 'photography', 'events', 'party',
               'fashion', 'culture', 'media', 'Capitol Hill', 'drinking', 'cocktail', 'clubbing',
               'dining', 'interior', 'travel', 'beach', 'surfing', 'vacation', 'events', 'honeymoon']
        objs = []
        for each_city in city:
            for each_tag in tag:
                objs += [[each_city, each_tag, am.ins_username, am.ins_fullname, am.ins_follower_count, am.ins_media_count, am.ins_biography, am.ins_external_url, am.ins_verified] for am in InstagramTracking.objects.filter(ins_biography__icontains=each_city).filter(ins_biography__icontains=each_tag)]
        print('Done')
        df = pd.DataFrame(objs)
        df.to_excel('Done.xlsx', index=False)

