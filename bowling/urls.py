from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^roll/$', views.roll, name='roll'),
    url(r'^roll/(?P<pins>[0-9]+)$', views.roll, name='roll_with_pins'),
    url(r'^start/$', views.start, name='start'),
    url(r'^total_score/$', views.total_score, name='total_score'),
    url(r'^total_score/(?P<player_id>[0-9]+)$', views.total_score, name='total_score_for_player_id'),
]
