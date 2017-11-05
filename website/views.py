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
                inputName = str(request.POST.get('inputName'))
            except:
                inputName = None
            try:
                inputEmail = str(request.POST.get('inputEmail'))
            except:
                inputEmail = None
            try:
                inputPartner = True if str(request.POST.get('inputPartner')) == "true" else False
                inputProduct = True if str(request.POST.get('inputProduct')) == "true" else False
                inputDetail = True if str(request.POST.get('inputDetail')) == "true" else False
            except:
                inputPartner = inputProduct = inputDetail = False

            try:
                inputMessage = str(request.POST.get('inputMessage'))
            except:
                inputMessage = None

            if inputEmail is not None and "@" in inputEmail and "." in inputEmail.split('@')[1]:
                nl_obj, created = ContactInfo.objects.get_or_create(contact_email=inputEmail)
                nl_obj.contact_name = inputName
                nl_obj.contact_content = inputMessage
                nl_obj.contact_is_partner = inputPartner
                nl_obj.contact_is_product = inputProduct
                nl_obj.contact_is_detail = inputDetail
                nl_obj.save()

                return JsonResponse({"result": "Successfully Added ✅"}, safe=False)
            else:
                return JsonResponse({"result": "Incorrect Email Format ❌"}, safe=False)
        except Exception as e:
            return JsonResponse({"result":"❌ Error: " + str(e)}, safe=False)
