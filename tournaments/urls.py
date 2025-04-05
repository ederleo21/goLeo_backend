from django.urls import path
from tournaments.views.general_views import TournamentListView, TournamentCreateView, TournamentUpdateAPIView, MatchDetailUpdateAPiView, AddPlayersToMatchView, MatchWithPlayersView, MatchScoreUpdateView, TournamentWithParticipantsView, MatchesByTournamentListCreateAPIView
from tournaments.views.league_views import  TournamentLeagueDetailView

urlpatterns = [
    #tournaments
    path('tournaments/', TournamentListView.as_view(), name='tournament_list'),
    path('tournament/create/', TournamentCreateView.as_view(), name='tournament_create'),
    path('tournament/update/<int:pk>/', TournamentUpdateAPIView.as_view(), name='tournament_update'),
    path('league/<int:id>/', TournamentLeagueDetailView.as_view(), name='tournament_detail'),
    
    #participaciones
    path('participations/create/', TournamentWithParticipantsView.as_view(), name="participantions_create"),

    #match
    path('matches/<int:tournament_id>/', MatchesByTournamentListCreateAPIView.as_view(), name='match_list'),
    path('matches/create/', MatchesByTournamentListCreateAPIView.as_view(), name='match_create'),
    path('match/<int:pk>/', MatchDetailUpdateAPiView.as_view(), name='match_detail'),
    path('match/participations_players/', AddPlayersToMatchView.as_view(), name='participations_players'),
    path('match/<int:match_id>/players/', MatchWithPlayersView.as_view(), name='match_with_players'), #GET PARA REGISTRO
    path('matches/<int:match_id>/update_score/', MatchScoreUpdateView.as_view(), name='update_match_score'),
]



