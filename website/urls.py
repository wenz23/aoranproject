from django.conf.urls import url
from django.views.generic import TemplateView

from gym import views as gview

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^gym-list/$', TemplateView.as_view(template_name="gym_list.html"), name='gym-list'),
    url(r'^get-gym-list/$', gview.gym_list_view)
]