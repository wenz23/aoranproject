import simplejson as json
from django.core.management.base import BaseCommand
from django.utils import timezone

from crawl.models import SocialDetails


def find_similars(source_type=None):
    starting_list_1 = [am.social_id for am in SocialDetails.objects.exclude(parse_state=600)]
    starting_list_2 = [json.loads(am.details)['similar_links'] for am in SocialDetails.objects.filter(parse_state=600)]

    starting_list = starting_list_1 + [item for sublist in starting_list_2 for item in sublist]

    for social_id in starting_list:
        if '/channel/' not in social_id:
            urldetail_obj, created = SocialDetails.objects.get_or_create(social_id=str(social_id).lower(),
                                                                         source_type=source_type,
                                                                         defaults={'created_at': timezone.now()})


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        find_similars('YouTube')
