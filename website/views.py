from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from website.models import ContactInfo


def home(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render)


def contact_form(request):
    if request.method == 'POST':
        try:
            contact_email = str(request.POST.get('contact_email'))
            if "@" in contact_email and "." in contact_email:
                nl_obj, created = ContactInfo.objects.get_or_create(contact_email)
                return JsonResponse("Successfully Added for " + contact_email, safe=False)
        except Exception as e:
            return JsonResponse("Error: " + str(e), safe=False)
