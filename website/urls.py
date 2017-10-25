from django.conf.urls import url
from django.views.generic import TemplateView
from website import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^contact-form/$', views.contact_form),

]
