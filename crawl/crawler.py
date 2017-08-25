import threading
import time
from datetime import date, timedelta
from json import loads, dumps
from queue import Queue
from threading import Thread
from django.db.models import Q
from django.db.models import Q
import requests
from django.utils import timezone

from crawl.models import InstagramMap, InstagramTracking
from crawl.models import StateEnum
from settings.production import api_gateway


def lambda_crawler_request(username=None, use_proxy=False, social_type=None):
    try:
        header = {'username': username,
                  'social_type': social_type,
                  'use_proxy': str(use_proxy),
                  'x-api-key': api_gateway['CrawlerAPIKey-C'][0]}

        req = requests.request('GET', url=api_gateway['CrawlerAPIKey-C'][1], headers=header, timeout=15, verify=False)
        if req.status_code == 200:
            return req.content
        else:
            return None
    except:
        return None


def crawl_ins_username_via_lambda(req_content=None, ins_map_obj=None):
    dictionary = loads(req_content)

    try:
        user_id = dictionary['entry_data']['ProfilePage'][0]['user']['id']
    except:
        user_id = None
    try:
        bio = dictionary['entry_data']['ProfilePage'][0]['user']['biography']
    except:
        bio = None
    try:
        username = dictionary['entry_data']['ProfilePage'][0]['user']['username']
    except:
        username = None

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

    if user_id and username:
        ins_tracking_obj = InstagramTracking(ins_id=user_id,
                                             ins_biography=bio,
                                             ins_external_url=ext_url,
                                             ins_follower_count=follower_count,
                                             ins_following_count=following_count,
                                             ins_recent_12_meta=dumps(recent_12),
                                             ins_fullname=full_name,
                                             ins_media_count=media_count,
                                             ins_verified=is_verified,
                                             ins_private=is_private,
                                             ins_json=dictionary,
                                             ins_username=username
                                             )
        ins_tracking_obj.save()
        ins_map_obj.latest_username = ins_tracking_obj.ins_username
        ins_map_obj.ins_id = ins_tracking_obj.ins_id
        ins_map_obj.latest_follower_count = ins_tracking_obj.ins_follower_count
        ins_map_obj.latest_crawl_state = StateEnum.Parse_Success
        ins_map_obj.latest_crawl_at = timezone.now()
        ins_map_obj.save()


def parse_ins_lambda_via_q(q):
    while not q.empty():

        ins_map_obj = q.get()

        # Request
        req_content = lambda_crawler_request(username=ins_map_obj.latest_username, social_type="ins")
        if req_content:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Success
            ins_map_obj.save()

            # Parse
            try:
                crawl_ins_username_via_lambda(req_content=req_content, ins_map_obj=ins_map_obj)
            except:
                ins_map_obj.latest_crawl_state = StateEnum.Parse_Failed
                ins_map_obj.save()

        else:
            ins_map_obj.latest_crawl_state = StateEnum.Req_Failed
            ins_map_obj.save()
        time.sleep(0.5)


def activate_ins_crawl(threads=20):
    """
    generate a list from Process Instagram to crawl, save result to Social Tracking
    :return:
    """

    prior_week = date.today() - timedelta(7)
    ins_to_crawl_list = [am for am in InstagramMap.objects.filter(
        Q(latest_crawl_state__in=[StateEnum.Parse_Failed, StateEnum.Req_Failed, StateEnum.New, StateEnum.Standby]) |
        Q(latest_crawl_state=StateEnum.Parse_Success, latest_crawl_at__gte=prior_week)
    )]

    q = Queue()
    for i in ins_to_crawl_list:
        q.put(i)

    sys_threads = threading.active_count()
    c = 0

    while not q.empty():
        try:
            c += 1
            tc = threading.active_count()
            if tc < (threads + sys_threads):
                print('Active Threads::' + str(tc))
                worker = Thread(target=parse_ins_lambda_via_q, args=(q,))
                worker.daemon = True
                worker.start()
                time.sleep(0.5)
            else:
                time.sleep(15)
        except Exception as e:
            print(e)

