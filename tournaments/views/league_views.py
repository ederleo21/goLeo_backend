from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from tournaments.models import Tournament
from tournaments.serializers.league_serializers import TournamentLeagueDetailSerializer

# Devuelve un torneo especifico con informacion de torneo league.
class TournamentLeagueDetailView(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentLeagueDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        tournament = self.get_object() 

        if tournament.type != 'LEAGUE':
            return Response({'detail': 'This tournament is not of type LEAGUE.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(tournament, context={'request': request})
        response_data = serializer.data

        return Response(response_data)