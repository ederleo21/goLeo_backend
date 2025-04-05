from rest_framework import serializers
from tournaments.models import League, Tournament
from core.models import Club

#Serializer de modelo liga
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['points_system', 'league_format', 'rounds', 'teams_count']


#Devolver information de un torneo tipo league
class TournamentLeagueDetailSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True) 
    clubs = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'type', 'start_date', 'end_date', 'photo', 'active', 'description', 'created', 'updated', 'league', 'clubs']

    def get_clubs(self, instance):
        from tournaments.serializers.general_serializers import ClubMinimalSerializer
        clubs = Club.objects.filter(id__in=instance.participants.values_list('club_id', flat=True))
        context = self.context  
        return ClubMinimalSerializer(clubs, many=True, context=context).data


#Crear torneo tipo liga
class CreateLeagueSerializer(serializers.ModelSerializer):
    tournament_id = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all(), source='tournament')

    class Meta:
        model = League
        fields = ['tournament_id', 'points_system', 'league_format']



