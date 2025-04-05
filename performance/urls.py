from django.urls import path
from .views import CreatePlayerStatisticsView, ListPlayerStatisticsView, UpdatePlayerStatisticsView, ListClubStatisticsView, DetailClubStatisticsView, MatchesCompletedTournamentView, PlayerTournamentStatsAPIView, StatisticsPlayerByTournamentAPIView, StatisticsForPlayerInTournamentAPIView

urlpatterns = [
    path('player-statistics/<int:match_id>/', ListPlayerStatisticsView.as_view(), name='list-player-statistics'),
    path('player-statistics/create/', CreatePlayerStatisticsView.as_view(), name='create-player-statistics'),
    path('player-statistics/<int:pk>/update/', UpdatePlayerStatisticsView.as_view(), name='update-player-statistics'),
    
    path('club-statistics/<int:tournament_id>/', ListClubStatisticsView.as_view(), name='list-club-statistics'),
    path('club-statistics/<int:club_id>/<int:tournament_id>/', DetailClubStatisticsView.as_view(), name='club-statistics'),

    path('matches/tournament/<int:tournament_id>/', MatchesCompletedTournamentView.as_view(), name='tournament_matches'),

    #Estadisticas a nivel de torneo
    path('statisticsPlayerByTournament/<int:pk>/', StatisticsPlayerByTournamentAPIView.as_view(), name='statisctis-player-tournament'),
    path('statisticsPlayerInTournament/<int:player_id>/<int:tournament_id>/', StatisticsForPlayerInTournamentAPIView.as_view(), name='statistics-player-in-tournament'),
    path('playerTournamentStats/<int:pk>/', PlayerTournamentStatsAPIView.as_view(), name='score'), #tops of players
]

