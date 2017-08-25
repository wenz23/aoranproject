import threading
import time
from datetime import date, timedelta
from json import loads
from queue import Queue
from threading import Thread

from aoranproject.common import lambda_crawler_request
from crawl.models import InstagramMap, InstagramTracking


def crawl_ins_username_via_lambda(ins_username=None):
    dictionary = loads(lambda_crawler_request(username=ins_username, use_proxy="False", social_type="ins"))
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
        st_obj = InstagramTracking(ins_id=user_id,
                                   ins_biography=bio,
                                   ins_external_url=ext_url,
                                   ins_follower_count=follower_count,
                                   ins_following_count=following_count,
                                   ins_recent_12_meta=loads(recent_12),
                                   ins_fullname=full_name,
                                   ins_media_count=media_count,
                                   ins_verified=is_verified,
                                   ins_private=is_private,
                                   ins_json=dictionary
                                   )
        st_obj.save()


def parse_ins_lambda_via_q(q):
    while not q.empty():
        ins_map_obj = q.get()


def generate_ins_crawl_list(threads=10):
    """
    generate a list from Process Instagram to crawl, save result to Social Tracking
    :return:
    """

    prior_week = date.today() - timedelta(7)
    ins_to_crawl_list = [am for am in InstagramMap.objects.filter(last_visited_at__gt=prior_week)]

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
                time.sleep(0.1)
            else:
                time.sleep(150)
        except Exception as e:
            print(e)

