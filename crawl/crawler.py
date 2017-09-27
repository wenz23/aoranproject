import threading
import time
from datetime import datetime
from json import loads, dumps
import random
import random

import requests
from django.utils import timezone

from crawl.models import InstagramTracking
from crawl.models import StateEnum
from settings.production import api_gateway


def lambda_crawler_request(username=None):

    try:
        if api == "C":
            api_key = api_gateway["CrawlerAPIKey-C"][0]
            api_url = api_gateway["CrawlerAPIKey-C"][1]
        else:
            api_key = api_gateway["CrawlerAPIKey-P"][0]
            api_url = api_gateway["CrawlerAPIKey-P"][1]
        header = {"username": username,
                  "x-api-key": api_key}

        req = requests.request('GET', url=api_url, headers=header, timeout=15, verify=False)
        if req.status_code == 200:
            return req.content
        else:
            return None
    except:
        return None


def thread_wrapper_for_q(thread_count=1, c_function=None, q=None, lock_main_thread=True, wait_time=5):
    worker = None
    if c_function and q:
        print("====================")
        print("Qsize count:")
        print(q.qsize())
        print("====================")
        for i in range(thread_count):
            if not q.empty():
                worker = threading.Thread(target=c_function, args=(q,))
                worker.daemon = False
                time.sleep(wait_time)
                worker.start()
                time.sleep(0.1)
            else:
                return True
        if lock_main_thread and worker:
            worker.join()


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

        # Growth Meta
        try:
            if ins_map_obj.ins_growth_meta:
                curr_dict = ins_map_obj.ins_growth_meta
                curr_dict[datetime.now().isoformat()] = int(following_count)
                ins_map_obj.ins_growth_meta = curr_dict
            else:
                ins_map_obj.ins_growth_meta = {datetime.now().isoformat(): int(following_count)}
        except Exception as e:
            print(e)
            pass

        # Growth Summary
        try:
            if ins_map_obj.ins_growth:
                curr_dict           = ins_map_obj.ins_growth
                start_d             = datetime.strptime(curr_dict['start']['d'], "%Y-%m-%dT%H:%M:%S.%f")
                start_c             = curr_dict['start']['c']
                end_d               = datetime.now()
                end_c               = int(following_count)
                curr_dict['end']    = {'d': end_d.isoformat(), 'c': end_c}
                if (end_d - start_d).days > 0:
                    curr_dict['rate']   = (end_c - start_c)/(end_d - start_d).days
                ins_map_obj.ins_growth = curr_dict
            else:
                ins_map_obj.ins_growth = {'start': {'d': datetime.now().isoformat(), 'c': int(following_count)}}

        except Exception as e:
            print(e)
            pass
        ins_map_obj.latest_username         = ins_tracking_obj.ins_username
        ins_map_obj.ins_id                  = ins_tracking_obj.ins_id
        ins_map_obj.latest_follower_count   = ins_tracking_obj.ins_follower_count
        ins_map_obj.latest_crawl_state      = StateEnum.Parse_Success
        ins_map_obj.latest_crawl_at         = timezone.now()
        ins_map_obj.save()
        return "Success"
    else:
        if dictionary['status code'] == '404':
            print("Parse Failed No User Name or ID. Username: 404:  ",
                  str(ins_map_obj.latest_username), "; Reason: ", dictionary)
            return "404"
        else:
            print("Parse Failed No User Name or ID. Username: ",
                  str(ins_map_obj.latest_username), "; Reason: ", dictionary)
            return "Other"
