from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.all, name='all stats'),
    url(r'^(?P<league_name>[A-Z]+)/$', views.league, name='league stats'),
    url(r'^(?P<player1>\w(_\w+)*)/compare/(?P<player2>\w+(_\w+)*)/$', views.compare, name='compare players'),
]