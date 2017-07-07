from aoranproject.common import api_gateway, lambda_crawler_request
from django.core.management.base import BaseCommand
import datetime
from json import loads
from crawl.models import SocialTracking


def get_ins_info_load_tracking_table(ins_username=None):
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
        is_verified = None
    try:
        is_private = dictionary['entry_data']['ProfilePage'][0]['user']['is_private']
    except:
        is_private = None
    try:
        recent_12 = dictionary['entry_data']['ProfilePage'][0]['user']['media']['nodes']
    except:
        recent_12 = None

    if user_id:
        st_obj = SocialTracking(ins_id=user_id, ins_biography=bio, ins_external_url=ext_url,
                                ins_follower_count=follower_count, ins_following_count=following_count,
                                ins_recent_12_meta=loads(recent_12), ins_fullname=full_name,
                                ins_post_count=media_count, ins)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        ins_username = "a.wen.z"

