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
            try:
                contact_email = str(request.POST.get('contact_email'))
            except:
                contact_email = None
            try:
                contact_type = str(request.POST.get('contact_type'))
            except:
                contact_type = None
            try:
                contact_name = str(request.POST.get('contact_name'))
            except:
                contact_name = None
            try:
                contact_content = str(request.POST.get('contact_content'))
            except:
                contact_content = None

            if contact_email is not None and "@" in contact_email and "." in contact_email:
                nl_obj, created = ContactInfo.objects.get_or_create(contact_email)

                return JsonResponse("Successfully Added ✅", safe=False)
            else:
                return JsonResponse("Incorrect Email Format ❌", safe=False)
        except Exception as e:
            return JsonResponse("❌ Error: " + str(e), safe=False)
