import numpy as np
import pandas as pd
import json
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        df = pd.read_csv('/Users/aoran/Desktop/googleMapDump.csv')
        for index, row in df.iterrows():
            name = str(row['name'])
            phone = str(row['phone'])
            website = str(row['website'])
            address = str(row['address'])
            description = str(row['description'])
            json_dict = json.loads(str(row['json']))
            map_url = str(row['map_url'])
            place_id = str(row['place_id'])
            query = json.loads(str(row['query']))
            try:
                rating = float(row['rating']) if float(row['rating']) == float(row['rating']) else None
            except:
                rating = None
            try:
                reviews = int(row['reviews'])
            except:
                reviews = None
            try:
                lat = json_dict['geometry']['location']['lat']
                lng = json_dict['geometry']['location']['lng']
            except:
                lat = None
                lng = None
            try:
                city = None
                state = None
                zip_code = None

                add_list = json_dict['address_components']
                for i in add_list:
                    if i['types'] == ['locality', 'political']:
                        city = i['long_name']
                    elif i['types'] ==['administrative_area_level_1', 'political']:
                        state = i['short_name']
                    elif i['types'] == ['postal_code']:
                        zip_code = i['short_name']

            print("Done")
