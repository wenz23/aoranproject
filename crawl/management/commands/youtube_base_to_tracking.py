import simplejson as json
from json import loads
from django.core.management.base import BaseCommand
from django.utils import timezone
from aoranproject.common import ins_clean_url
from crawl.models import YouTubeDetails, SocialTracking
from aoranproject.common import lambda_crawler_request
import threading
import time
from queue import Queue
from threading import Thread

import requests
import simplejson as json
import urllib3
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone


def find_similars(source_type=None):
    starting_list_1 = [am.social_id for am in YouTubeDetails.objects.exclude(parse_state=600)]

    starting_list_2 = [json.loads(am.details)['similar_links'] for am in YouTubeDetails.objects.filter(parse_state=600)]

    starting_list = starting_list_1 + [item for sublist in starting_list_2 for item in sublist]

    for social_id in starting_list:
        if '/channel/' not in social_id:
            urldetail_obj, created = YouTubeDetails.objects.get_or_create(social_id=str(social_id).lower(),
                                                                          source_type=source_type,
                                                                          defaults={'created_at': timezone.now()})


def get_ins_info_load_tracking_table(ins_username=None):
    req = lambda_crawler_request(username=ins_username, use_proxy="False", social_type="ins")
    dictionary = loads(req.content)

    try:
        user_id = dictionary['entry_data']['ProfilePage'][0]['user']['id']
    except:
        user_id = None
    try:
        bio = dictionary['entry_data']['ProfilePage'][0]['user']['biography']
    except:
        bio = None
    try:
        ext_url = dictionary['entry_data']['ProfilePage'][0]['user']['external_url']
    except:
        ext_url = None
    try:
        follower_count = dictionary['entry_data']['ProfilePage'][0]['user']['followed_by']['count']
    except:
        follower_count = None
    try:
        following_count = dictionary['entry_data']['ProfilePage'][0]['user']['follows']['count']
    except:
        following_count = None
    try:
        full_name = dictionary['entry_data']['ProfilePage'][0]['user']['full_name']
    except:
        full_name = None
    try:
        media_count = dictionary['entry_data']['ProfilePage'][0]['user']['media']['count']
    except:
        media_count = None
    try:
        is_verified = dictionary['entry_data']['ProfilePage'][0]['user']['is_verified']
    except:
        is_verified = False
    try:
        is_private = dictionary['entry_data']['ProfilePage'][0]['user']['is_private']
    except:
        is_private = False
    try:
        recent_12 = dictionary['entry_data']['ProfilePage'][0]['user']['media']['nodes']
    except:
        recent_12 = None

    if user_id:
        # 1
        st_obj, created = SocialTracking.objects.get_or_create(ins_id=user_id)
        if created:
            st_obj.ins_biography = bio
            st_obj.url = str('https://www.instagram.com/')+str(ins_username)+str('/')
            st_obj.ins_username = str(ins_username)
            st_obj.social_media_type = 'Instagram'
            st_obj.ins_external_url = ext_url
            st_obj.ins_follower_count = follower_count
            st_obj.ins_following_count = following_count
            st_obj.ins_recent_12_meta = json.dumps(recent_12)
            st_obj.ins_fullname=full_name
            st_obj.ins_media_count=media_count
            st_obj.ins_verified=is_verified
            st_obj.ins_private=is_private
            st_obj.ins_json=dictionary
            st_obj.save()

        # 2
        # st_obj = SocialTracking(ins_id=user_id, ins_biography=bio, ins_external_url=ext_url,
        #                         ins_follower_count=follower_count, ins_following_count=following_count,
        #                         ins_recent_12_meta=json.dumps(recent_12), ins_fullname=full_name,
        #                         ins_media_count=media_count, ins_verified=is_verified, ins_private=is_private,
        #                         ins_json=dictionary)
        # st_obj.save()


def request_via_q(q):
    while not q.empty():

        # Create social detail object
        i = q.get()
        get_ins_info_load_tracking_table(i)
        if q.qsize() % 20 == 0:
            print("Q Size # ", q.qsize())
    return True


def load_new_ins_user_to_tracking_table():
    new_ins_user_list = []
    starting_list_temp = [json.loads(am.details)['related_links'] for am in YouTubeDetails.objects.filter(parse_state=600)]
    starting_list = [item for sublist in starting_list_temp for item in sublist]

    for i in starting_list:
        if str('www.instagram.com') in i:
            clean_url = ins_clean_url(url=i, return_id=True)
            if clean_url is not None:
                new_ins_user_list.append(clean_url)
    new_ins_user_list = list(set(new_ins_user_list))

    q = Queue()
    for i in new_ins_user_list:
        q.put(i)
    print("Starting Queue Size # ", q.qsize())

    # setting up queue
    sys_threads = threading.active_count()
    threads = 50
    c = 0
    while not q.empty():
        try:
            c += 1
            tc = threading.active_count()
            if tc < (threads + sys_threads):
                print('Active Threads::' + str(tc))
                worker = Thread(target=request_via_q, args=(q,))
                worker.daemon = True
                worker.start()
                time.sleep(0.1)
            else:
                time.sleep(190)
        except Exception as e:
            print(e)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # find_similars('YouTube')
        load_new_ins_user_to_tracking_table()
