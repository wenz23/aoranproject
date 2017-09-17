from django.http import JsonResponse

from gym.models import Gyms


def gym_list_view(request):
    if request.method == 'GET':
        gyms = [[am.gym_name, am.street_address, am.zip_code, am.phone, am.revisited_at.date().isoformat(), am.gym_url] for am in Gyms.objects.all()]

        return JsonResponse(gyms, safe=False)


