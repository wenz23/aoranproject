import simplejson as json
from django.core.management.base import BaseCommand
from django.utils import timezone
from aoranproject.common import ins_clean_url
from crawl.models import YouTubeDetails


def find_similars(source_type=None):
    starting_list_1 = [am.social_id for am in YouTubeDetails.objects.exclude(parse_state=600)]

    starting_list_2 = [json.loads(am.details)['similar_links'] for am in YouTubeDetails.objects.filter(parse_state=600)]

    starting_list = starting_list_1 + [item for sublist in starting_list_2 for item in sublist]

    for social_id in starting_list:
        if '/channel/' not in social_id:
            urldetail_obj, created = YouTubeDetails.objects.get_or_create(social_id=str(social_id).lower(),
                                                                          source_type=source_type,
                                                                          defaults={'created_at': timezone.now()})


def load_new_ins_user_to_tracking_table():
    new_ins_user_list = []
    starting_list_temp = [json.loads(am.details)['related_links'] for am in YouTubeDetails.objects.filter(parse_state=600)]
    starting_list = [item for sublist in starting_list_temp for item in sublist]

    for i in starting_list:
        if str('www.instagram.com') in i:
            clean_url = ins_clean_url(url=i)
            if clean_url is not None and clean_url != str('https://www.instagram.com//'):
                new_ins_user_list.append(clean_url)
    new_ins_user_list = list(set(new_ins_user_list))

    for i in new_ins_user_list:



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # find_similars('YouTube')
        load_new_ins_user_to_tracking_table()
