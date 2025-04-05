from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from tournaments.models import Tournament
from tournaments.serializers.general_serializers import TournamentSerializer

