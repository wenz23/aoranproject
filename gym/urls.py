from django.conf.urls import url
from django.views.generic import TemplateView
from gym import views

urlpatterns = [
    url(r'^gym-list/$', TemplateView.as_view(template_name="gym-list.html"), name='gym-list'),

    url(r'^get-gym-list/$', views.gym_list_view)
]