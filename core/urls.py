from django.urls import path
from .views.clubs import ClubListView, ClubCreateView, ClubDetailView, ClubUpdateView, ClubDeleteView
from .views.players import PlayerListView, PlayerCreateView, PlayerSkillCreateView, PlayerDetailView, PlayerUpdateView, PlayerSkillUpdateView, PlayerDeleteView
from .views.position import PositionListView
from .views.country import CountryListView
from .views.user import UpdateUserView

urlpatterns = [
    #API CLUBS
    path('clubs/', ClubListView.as_view(), name='clubs'),
    path('clubs/create/', ClubCreateView.as_view(), name='clubs_create'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<int:pk>/update/', ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', ClubDeleteView.as_view(), name='club_delete'),

    #API PLAYERS
    path('players/', PlayerListView.as_view(), name='players'),
    path('players/create/', PlayerCreateView.as_view(), name='player_create'),
    path('skills/create/', PlayerSkillCreateView.as_view(), name='skills_create'),
    path('players/<int:id>/update/', PlayerUpdateView.as_view(), name='player_update'),
    path('skills/<int:player__id>/update/', PlayerSkillUpdateView.as_view(), name='skills_update'),
    path('players/<int:pk>/delete/', PlayerDeleteView.as_view(), name='player_delete'), 
    path('players/<int:id>/', PlayerDetailView.as_view(), name='player_detail'),

    #API POSITION
    path('positions/', PositionListView.as_view(), name='positions'),

    #API COUNTRY
    path('countries/', CountryListView.as_view(), name='countries'),

    #API USER
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='user_update'),
]



