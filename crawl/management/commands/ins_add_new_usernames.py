
from django.utils import timezone
from crawl.models import InstagramMap
from django.core.management.base import BaseCommand


def new_project(project_name=None, new_list=None):
    for new_username in new_list:
        map_obj, created = InstagramMap.objects.get_or_create(latest_username=new_username)

        if created:
            map_obj.project_info = {project_name: timezone.now().isoformat()}
        else:
            temp_dict = map_obj.project_info
            temp_dict[project_name] = timezone.now().isoformat()
            map_obj.project_info = temp_dict
        map_obj.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        new_project_name = "project_a"
        new_list = ["ernestalexander", "warbyparker", "pladra", "shopacrimony", "garrettleight", "makerandmoss",
                    "plantationdesign", "azaleasf", "buloshoes", "randandstatler", "stevenalan", "ofinajewelry",
                    "aetherapparel", "marinelayer", "seldomseen", "gathersf", "timbuk2", "convertberkeley",
                    "flight001", "willleathergoods", "carylane"]

        new_project(project_name=new_project_name, new_list=new_list)
