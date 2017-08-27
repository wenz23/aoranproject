from json import loads, dumps

import requests
from django.utils import timezone

from crawl.models import InstagramTracking
from crawl.models import StateEnum
from settings.production import api_gateway


def lambda_crawler_request(username=None):
    try:
        header = {"username": username,
                  "x-api-key": api_gateway["CrawlerAPIKey-C"][0]}

        req = requests.request('GET', url=api_gateway["CrawlerAPIKey-C"][1], headers=header, timeout=15, verify=False)
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
        return "Success"
    else:
        print("Parse Failed No User Name or ID. Username: ",
              str(ins_map_obj.latest_username), "; Reason: ", dictionary)
        return None
