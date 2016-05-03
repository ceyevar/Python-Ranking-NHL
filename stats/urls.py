from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.all, name='all stats'),
    url(r'^(?P<league_name>[A-Z]+)/$', views.league, name='league stats'),
    url(r'^teams/(?P<team_id>[0-9]+)/$', views.team, name='team stats'),
    url(r'^players/(?P<player_id>[0-9]+)/$', views.player, name='player stats'),
    url(r'^players/(?P<player1_id>[0-9]+)/compare/(?P<player2_id>[0-9]+)/$', views.compare_players, name='compare players'),
    url(r'^teams/myteam/$', views.team_builder, name='team stats'),
    url(r'^teams/rankings/$', views.rankings, name='team stats'),
    url(r'^teams/myteam/add/(?P<playerid>[0-9]+)/$', views.add_player, name='team stats'),
    url(r'^teams/myteam/remove/(?P<playerid>[0-9]+)/$', views.remove_player, name='team stats'),
]