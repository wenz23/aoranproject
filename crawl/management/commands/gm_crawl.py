from django.core.management.base import BaseCommand
from crawl.integration.google_map_workflow import GoogleMapParser


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
