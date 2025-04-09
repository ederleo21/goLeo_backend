from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import CreatePlayerStatisticsSerializer, ClubStatisticsSerializer, ListPlayerStatisticsSerializer, MatchesByTournamentSerializer, UpdatePlayerStatisticsSerializer
from .models import PlayerStatistics, ClubStatistics
from rest_framework.permissions import IsAuthenticated, AllowAny 
from tournaments.models import Participation, Tournament, Match, PlayerParticipation
from tournaments.serializers.general_serializers import MatchSerializer
from django.db.models import Count, Min, Max, Avg, Sum
from django.conf import settings
from django.shortcuts import get_object_or_404

#Registrar estadísticas de los jugadores en un partido
class CreatePlayerStatisticsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Se esperaba una lista de estadísticas."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreatePlayerStatisticsSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Estadísticas registradas correctamente"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

#Obtener estadisticas de jugadores en un partido
class ListPlayerStatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, match_id):
        match = Match.objects.filter(pk=match_id).first()
        if not match:
            return Response({"error": "partido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        match_serializer = MatchSerializer(match, context={'request': request})

        home_team_statistics = PlayerStatistics.objects.filter(
            player_participation__match=match,
            player_participation__player__club=match.home_team
            )
        home_team_statistics_serializer = ListPlayerStatisticsSerializer(home_team_statistics, many=True, context={'request': request})

        away_team_statistics = PlayerStatistics.objects.filter(
            player_participation__match=match,
            player_participation__player__club=match.away_team
        )
        away_team_statistics_serializer = ListPlayerStatisticsSerializer(away_team_statistics, many=True, context={'request': request})

        return Response({**match_serializer.data, "home_team_statistics": home_team_statistics_serializer.data, "away_team_statistics": away_team_statistics_serializer.data}, status=status.HTTP_200_OK)


#Actualizar estadisticas de los jugadores en un partido
class UpdatePlayerStatisticsView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        statistics = PlayerStatistics.objects.filter(pk=pk).first()
        if not statistics:
            return Response({"error": "Estadísticas no encontradas"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdatePlayerStatisticsSerializer(statistics, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener estadisticas de clubes en un torneo 
class ListClubStatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tournament_id):
        clubs_statistics = ClubStatistics.objects.filter(participation__tournament=tournament_id)
        clubs_statistics = clubs_statistics.order_by('-total_wins')
        clubs_statistics_serializer = ClubStatisticsSerializer(clubs_statistics, many=True, context={'request': request})
        return Response(clubs_statistics_serializer.data, status=status.HTTP_200_OK)


#Obtener las estadisticas de un club en un torneo
class DetailClubStatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, club_id, tournament_id):
        participation = Participation.objects.filter(club_id=club_id, tournament_id=tournament_id).first()
        if not participation:
            return Response({"error": "La participacion no existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        club_statistics = ClubStatistics.objects.filter(participation=participation).first()
        if not club_statistics:
            return Response({"error": "No existe estadísticas para este club"}, status=status.HTTP_404_NOT_FOUND)

        club_statistics_serializer = ClubStatisticsSerializer(club_statistics, context={"request": request})
        return Response(club_statistics_serializer.data, status=status.HTTP_200_OK)


class MatchesCompletedTournamentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tournament_id):
        tournament = Tournament.objects.filter(pk=tournament_id).first()
        if not tournament:
            return Response({"error": "Torneo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        matches = Match.objects.filter(tournament=tournament, state='COMPLETED')
        
        if not matches.exists():
            return Response({"message": "No hay partidos completados para este torneo."}, status=status.HTTP_200_OK)

        serializer = MatchSerializer(matches, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#Vista de tops de player a nivel de torneo

class PlayerTournamentStatsAPIView(APIView):
    permission_classes = [AllowAny]

    CLOUDINARY_BASE_URL = "https://res.cloudinary.com/djretqgrx/image/upload/v1/"

    def get(self, request, pk):

        def process_players(players):
            for player in players:
                path = player.get('player_participation__player__photo')
                if path:
                    player['player_photo_url'] = f"{self.CLOUDINARY_BASE_URL}{path}"
                else:
                    player['player_photo_url'] = None
            return players

        common_fields = [
            "player_participation__player__first_name",
            "player_participation__player__id",
            "player_participation__player__club__name",
            "player_participation__player__last_name",
            "player_participation__player__photo"
        ]

        max_player_goals = (
            PlayerStatistics.objects
            .filter(player_participation__match__tournament=pk)
            .values(*common_fields)
            .annotate(total_goals=Sum("goals_scored"))
            .order_by('-total_goals')[:3]
        )

        max_player_assists = (
            PlayerStatistics.objects
            .filter(player_participation__match__tournament=pk)
            .values(*common_fields)
            .annotate(total_assists=Sum("assists"))
            .order_by('-total_assists')[:3]
        )

        max_player_recoveries = (
            PlayerStatistics.objects
            .filter(player_participation__match__tournament=pk)
            .values(*common_fields)
            .annotate(total_recoveries=Sum("ball_recoveries"))
            .order_by('-total_recoveries')[:3]
        )

        max_player_saves = (
            PlayerStatistics.objects
            .filter(player_participation__match__tournament=pk)
            .values(*common_fields)
            .annotate(total_saves=Sum("saves"))
            .order_by('-total_saves')[:3]
        )

        return Response({
            "top_goalscorers": process_players(max_player_goals),
            "top_assists": process_players(max_player_assists),
            "top_recoveries": process_players(max_player_recoveries),
            "top_saves": process_players(max_player_saves)
        })

#Vista para tabla resumida de estadisticas de jugadores.
class StatisticsPlayerByTournamentAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        players = PlayerParticipation.objects.filter(match__tournament=pk)
        player_stats = PlayerStatistics.objects.filter(player_participation__in=players)
        
        accumulated_stats = {}
        for stat in player_stats:
            player_id = stat.player_participation.player.id
            player_name = f"{stat.player_participation.player.first_name} {stat.player_participation.player.last_name}"
            player_club_name = stat.player_participation.player.club.name
            player_club_id = stat.player_participation.player.club.id
            
            if player_id not in accumulated_stats:
                accumulated_stats[player_id] = {
                    'player': player_name,
                    'player_id': player_id,
                    'player_club_name': player_club_name,
                    'player_club_id': player_club_id,
                    'goals_scored': 0,
                    'assists': 0,
                }
            
            accumulated_stats[player_id]['goals_scored'] += stat.goals_scored
            accumulated_stats[player_id]['assists'] += stat.assists
        
        player_data = list(accumulated_stats.values())
        return Response(player_data, status=status.HTTP_200_OK)
    

#Vista para brindar informacion completa de un jugador en un torneo.
class StatisticsForPlayerInTournamentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, player_id, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)
        player_participations = PlayerParticipation.objects.filter(match__tournament=tournament, player_id=player_id)

        if not player_participations.exists():
            return Response({"error": "El jugador no participó en este torneo."}, status=status.HTTP_404_NOT_FOUND)
        
        player_stats = PlayerStatistics.objects.filter(player_participation__in=player_participations)
        player = player_participations.first().player
        player_id = player_participations.first().player.id
        photo_url = request.build_absolute_uri(player.photo.url) if player.photo else None
        photo_club_url = request.build_absolute_uri(player.club.logo.url) if player.club.logo.url else None

        accumulated_stats = {
            'player': f"{player.first_name} {player.last_name}",
            'player_id': player_id,
            'player_photo': photo_url,
            'player_club_name': player.club.name,
            'player_club_logo': photo_club_url,
            'player_position': player.position.description,
            'matches_played': player_participations.count(),
            'goals_scored': 0,
            'assists': 0,
            'shots_on_target': 0,
            'completed_passes': 0,
            'duel_wins': 0,
            'ball_recoveries': 0,
            'blocks': 0,
            'fouls_drawn': 0,
            'fouls_committed': 0,
            'yellow_cards': 0,
            'red_cards': 0,
            'saves': 0
        }

        for stat in player_stats:
            accumulated_stats['goals_scored'] += stat.goals_scored
            accumulated_stats['assists'] += stat.assists
            accumulated_stats['shots_on_target'] += stat.shots_on_target
            accumulated_stats['completed_passes'] += stat.completed_passes
            accumulated_stats['duel_wins'] += stat.duel_wins
            accumulated_stats['ball_recoveries'] += stat.ball_recoveries
            accumulated_stats['blocks'] += stat.blocks
            accumulated_stats['fouls_drawn'] += stat.fouls_drawn
            accumulated_stats['fouls_committed'] += stat.fouls_committed
            accumulated_stats['yellow_cards'] += stat.yellow_cards
            accumulated_stats['red_cards'] += stat.red_cards
            accumulated_stats['saves'] += stat.saves

        return Response(accumulated_stats, status=status.HTTP_200_OK)



