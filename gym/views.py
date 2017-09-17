from django.http import JsonResponse

from gym.models import Gyms


def gym_list_view(request):
    if request.method == 'GET':
        gyms = [[am.gym_name, am.gym_url, am.street_address, am.zip_code, am.phone, am.revisited_at] for am in Gyms.objects.all()]

        return JsonResponse(gyms, safe=False)


