from django.shortcuts import get_object_or_404
import json
from datetime import datetime
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from tournaments.models import Tournament, Match, PlayerParticipation
from tournaments.serializers.general_serializers import TournamentSerializer, CreateTournamentSerializer, MatchSerializer, TournamentWithParticipantsSerializer, PlayerParticipationSerializer, MatchWithPlayersGroupedSerializer, MatchScoreUpdateSerializer
from tournaments.serializers.league_serializers import CreateLeagueSerializer 
from tournaments.serializers.cup_serializers import CreateCupSerializer
from performance.utils import update_club_statistics

#Listar de torneos de tipo tipo
class TournamentListView(generics.ListAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tournament_id = self.request.query_params.get('id', None)
        if tournament_id is not None:
            return Tournament.objects.filter(id=tournament_id)
        else:
            return Tournament.objects.all()


#Crear un torneo, se ajusta dinamicamente a informacion exclusiva de cualquier tipo
class TournamentCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        tournament_serializer = CreateTournamentSerializer(data=request.data)

        if tournament_serializer.is_valid():
            tournament = tournament_serializer.save()
            tournament_type = tournament.type
            
            additional_data = request.data.get("additional_data", None)
            if additional_data:
                additional_data = json.loads(additional_data) 

            tournament_data = {"id": tournament.id, **tournament_serializer.data}  

            if tournament_type == "LEAGUE" and additional_data:
                league_data = {
                    "tournament_id": tournament.id,
                    **additional_data
                }
                league_serializer = CreateLeagueSerializer(data=league_data)
                if league_serializer.is_valid():
                    league_serializer.save()
                    tournament_data.update(league_serializer.data)
                else:
                    return Response(league_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif tournament_type == "CUP" and additional_data:
                cup_data = {
                    "tournament_id": tournament.id,
                    **additional_data
                }
                cup_serializer = CreateCupSerializer(data=cup_data)
                if cup_serializer.is_valid():
                    cup_serializer.save()
                    tournament_data.update(cup_serializer.data)

                else:
                    return Response(cup_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(tournament_data, status=status.HTTP_201_CREATED)
        return Response(tournament_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Actualizar información general de un torneo
class TournamentUpdateAPIView(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [AllowAny]


class MatchesByTournamentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        return Match.objects.filter(tournament_id=tournament_id)


class MatchDetailUpdateAPiView(generics.RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]


#Registro de clubes a un torneo, mediante una lista
class TournamentWithParticipantsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TournamentWithParticipantsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Participations creadas con éxito"}, status=status.HTTP_201_CREATED)


#Registro de jugadores en un partido
class AddPlayersToMatchView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        match_id = request.data.get('match_id')
        player_ids = request.data.get('players', [])
        match = Match.objects.filter(id=match_id).first()

        if not match:
            return Response({'detail': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        if not player_ids:
            return Response({'detail': 'Debe enviar una lista de jugadores'}, status=status.HTTP_400_BAD_REQUEST)
        
        participations = []
        for player_id in player_ids:
            participation = PlayerParticipation.objects.create(match=match, player_id=player_id)
            participations.append(participation)
        
        match.state = 'IN_PROGRESS'
        match.save()
        participation_serializer = PlayerParticipationSerializer(participations, many=True)
        return Response(participation_serializer.data, status=status.HTTP_201_CREATED)


#Devolver partidos con informacion de club y sus jugadores, usado para crear formulario de registro de estadisticas
class MatchWithPlayersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, id=match_id)
        serializer = MatchWithPlayersGroupedSerializer(match, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#Registro y actualizacion de marcador de partido
class MatchScoreUpdateView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, match_id):
        match = Match.objects.filter(id=match_id).first()
        tournament = match.tournament
        if not match:
            return Response({"error": "Partido no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        previous_score_home = match.score_home
        previous_score_away = match.score_away
        
        serializer = MatchScoreUpdateSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()   

            if match.state != "COMPLETED":

                if not (match.round == 0 and tournament.type == "LEAGUE"):
                    update_club_statistics(match, previous_score_home, previous_score_away)

                match.state = "COMPLETED"
                tournament = match.tournament
                if tournament.type == "LEAGUE" and not match.date:
                    match.date = datetime.now().date()
                match.save()
                
            else:
                if not (match.round == 0 and tournament.type == "LEAGUE"):
                    update_club_statistics(match, previous_score_home, previous_score_away)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


