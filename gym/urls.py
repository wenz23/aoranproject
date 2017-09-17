from django.conf.urls import url
from django.views.generic import TemplateView
from gym import views

urlpatterns = [
    url(r'^get-gym-list/$', views.gym_list_view)
]