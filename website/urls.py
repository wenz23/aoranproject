from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^gym-list/$', TemplateView.as_view(template_name="gym/gym-list.html"), name='gym-list'),
]