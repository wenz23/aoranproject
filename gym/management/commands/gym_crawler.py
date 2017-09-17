# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import phonenumbers
from django.utils import timezone
from gym.models import Gyms

import usaddress

def gym_homepage():
    home_url = "http://www.planetfitness.com/all-clubs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Accept-Language": "en"
    }

    home_req = requests.get(url=home_url, headers=headers)
    home_soup = BeautifulSoup(home_req.content, "html.parser")
    gym_urls = ["http://www.planetfitness.com" + am.get('href') for am in
                home_soup.find("div", {"class": "all_clubs-listings"}).find_all("a", {"class": "club-listing"})]
    return gym_urls



def parse_individual_gym(each_url=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Accept-Language": "en"
    }
    each_req = requests.get(url=each_url, headers=headers, timeout=8, allow_redirects=False)
    each_soup = BeautifulSoup(each_req.content, "html.parser")

    # parse
    try:
        store_name = each_soup.find("h1", {"class": "title"}).text
    except:
        store_name = None
    try:
        address = each_soup.find("div", {"class": "gym-header"}).find("div", {"class": "address"}).text
        try:
            add_dict = usaddress.tag(address)
            city = add_dict[0]["PlaceName"]
            zipcode = add_dict[0]["ZipCode"]
            state = add_dict[0]["StateName"]
        except:
            address = None
            add_dict = None
            city = None
            zipcode = None
            state = None
    except:
        address = None
        add_dict = None
        city = None
        zipcode = None
        state = None
    try:
        phone = each_soup.find("div", class_="views-field-phone").find_all("span")[1].text
    except:
        phone = None
    try:
        hours = each_soup.find("div", class_="views-field-field-hours").text
    except:
        hours = None
    try:
        holiday_hours = each_soup.find("div", class_="views-field-field-holidays-compiled").text
    except:
        holiday_hours = None

    try:
        gym_obj, created = Gyms.objects.get_or_create(gym_url=each_url)

        if not created:
            gym_obj.revisited_at = timezone.now()
        gym_obj.street_address = address
        gym_obj.city = city
        gym_obj.state = state
        gym_obj.zip_code = zipcode
        gym_obj.hours = hours
        gym_obj.holiday = holiday_hours
        gym_obj.gym_url = each_url
        gym_obj.phone = phone
        gym_obj.gym_name = store_name
        gym_obj.save()

    except Exception as e:
        print(e)




    print("Done")



class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        gym_urls = gym_homepage()
        for each_url in gym_urls:
            parse_individual_gym(each_url=each_url)
