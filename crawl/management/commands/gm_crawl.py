from django.core.management.base import BaseCommand

from datetime import datetime
import time
import googlemaps

from crawl.models import GoogleMap


class GoogleMapParser:

    def __init__(self):
        self.key = 'AIzaSyDbP810QmlsElSSd3E6R5eJq75lgyChLp0' # AIzaSyDbP810QmlsElSSd3E6R5eJq75lgyChLp0  AIzaSyDHcCKq5fKSIWYejt8PF0cO6P81L13xlcs
        self.g_maps = googlemaps.Client(key=self.key)
        self.geo_dict = {}

    def get_city_geocode(self, cities=None):
        geo_dict = {}
        for city in cities:
            time.sleep(0.5)
            city_geocode = self.g_maps.geocode(city)
            lat_ne = city_geocode[0]['geometry']['viewport']['northeast']['lat']
            lat_sw = city_geocode[0]['geometry']['viewport']['southwest']['lat']
            lat_ct = (lat_ne + lat_sw) / 2

            lng_ne = city_geocode[0]['geometry']['viewport']['northeast']['lng']
            lng_sw = city_geocode[0]['geometry']['viewport']['southwest']['lng']
            lng_ct = (lng_ne + lng_sw) / 2

            geo_dict[city] = {'ct': {'lat': lat_ct, 'lng': lng_ct},
                              # 'ne': {'lat': lat_ne, 'lng': lng_ne},
                              # 'sw': {'lat': lat_sw, 'lng': lng_sw},
                              # 'nw': {'lat': lat_ne, 'lng': lng_sw},
                              # 'se': {'lat': lat_sw, 'lng': lng_ne}
                              }

        self.geo_dict = geo_dict

    def search_place(self, queries=None):
        city_geo_dict = self.geo_dict
        for query in queries:
            for key in city_geo_dict:
                geo_dict = city_geo_dict[key]
                for viewport in geo_dict:
                    lat_lng = str(geo_dict[viewport]['lat']) + ", " + str(geo_dict[viewport]['lng'])

                    next_page_token = ""
                    while next_page_token is not None:
                        results = self.g_maps.places(query=query, location=lat_lng, radius=50000, page_token=next_page_token)
                        results = results['results']

                        for result in results:
                            place_id = result['place_id']
                            gm_obj, created = GoogleMap.objects.get_or_create(place_id=place_id)
                            if gm_obj.query is None or gm_obj.query == {}:
                                gm_obj.query = {datetime.now().isoformat(): {'query': query, 'city': key}}
                            else:
                                temp_dict = gm_obj.query
                                temp_dict[datetime.now().isoformat()] = {'query': query, 'city': key}
                            gm_obj.save()

                        try:
                            next_page_token = results['next_page_token']
                        except:
                            next_page_token = None

    def get_place_details(self):
        places = [am for am in GoogleMap.objects.filter(place_id__isnull=False)]
        for place in places:
            result = self.g_maps.place(place.place_id)['result']
            try:
                place.map_url = result['url']
            except:
                pass
            try:
                place.name = result['name']
            except:
                pass
            try:
                place.rating = result['rating']
            except:
                pass
            try:
                place.reviews = len(result['reviews'])
            except:
                pass
            try:
                place.address = result['formatted_address']
            except:
                pass
            try:
                place.phone = result['formatted_phone_number']
            except:
                pass
            try:
                place.website = result['website']
            except:
                pass
            try:
                place.description = '; '.join(result['types'])
            except:
                pass
            place.json = result
            try:
                place.save()
            except Exception as e:
                print(str(e))
                pass


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        top_us_cities = ['San Francisco, CA',
                         'New York, NY',
                         'Los Angeles, CA',
                         'Chicago, IL',
                         'Houston, TX',
                         'Phoenix, AZ',
                         'Philadelphia, PA',
                         'San Antonio, TX',
                         'San Diego, CA',
                         'Dallas, TX',
                         'San Jose, CA',
                         'Austin, TX',
                         'Seattle, WA',
                         'Portland, OR',
                         'Long Beach, CA',
                         'Irvine, CA',
                         'Miami, FL',
                         'Charlotte, NC',
                         'Denver, CO',
                         'Washington, DC',
                         'Boston, MA',
                         'Memphis, TN',
                         'Albuquerque, NM',
                         'Atlanta, GA',
                         'Newport Beach, CA',
                         'New Orleans, LA',
                         'Honolulu, HI',
                         'St. Louis, MO',
                         'Reno, NV',
                         'Boise, ID',
                         'Salt Lake City, UT',
                         'Las Vegas, NV',
                         'Milwaukee, WI',
                         'Tucson, AZ',
                         'Fresno, CA',
                         'Sacramento, CA',
                         'Colorado Springs, CO',
                         'Virginia Beach, VA',
                         'Oakland, CA',
                         'Minneapolis, MN',
                         'Kansas City, MO',
                         'Arlington, VA',
                         'Wichita, KS',
                         'Cleveland, OH',
                         'Tampa, FL',
                         'Bakersfield, CA',
                         'Pittsburgh, PA',
                         'Orlando, FL',
                         'Durham, NC']
        queries = ['Clothing Store',
                   'Boutique shop',
                   'boutique fashion',
                   'shoe store'
                   'Designer',
                   'Fashion Store']

        gmap = GoogleMapParser()
        gmap.get_city_geocode(cities=top_us_cities)
        gmap.search_place(queries=queries)
        gmap.get_place_details()
