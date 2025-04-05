from rest_framework import serializers 
from django.conf import settings
from .models import PlayerStatistics, ClubStatistics
from core.models import Club
from tournaments.models import Match

#Registrar estadisticas de los jugadores en un partido
class CreatePlayerStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatistics
        fields = '__all__'
    
    def validate_player_participation(self, value):
        if PlayerStatistics.objects.filter(player_participation=value).exists():
            raise serializers.ValidationError(f"Ya existen estadísticas para la participación {value.id}.")
        return value
    

#Obtener lista de estadisticas de jugadores en un partido
class ListPlayerStatisticsSerializer(serializers.ModelSerializer):
    player_first_name = serializers.CharField(source='player_participation.player.first_name', read_only=True)
    player_last_name = serializers.CharField(source='player_participation.player.last_name', read_only=True)
    player_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayerStatistics
        fields = ['id', 'player_first_name', 'player_last_name', 'player_photo', 'goals_scored', 'assists', 'shots_on_target', 'completed_passes', 'duel_wins', 'ball_recoveries', 'blocks', 'fouls_drawn', 'fouls_committed', 'yellow_cards', 'red_cards', 'saves']

    def get_player_photo(self, obj):
        request = self.context.get('request')
        if hasattr(obj.player_participation.player, 'photo') and obj.player_participation.player.photo:
            photo_url = obj.player_participation.player.photo.url
            return request.build_absolute_uri(photo_url) if request else f"{settings.MEDIA_URL}{photo_url}"
        return None


#Actualizar estadistica de jugador
class UpdatePlayerStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatistics
        fields = ['goals_scored', 'assists', 'shots_on_target', 'completed_passes', 'duel_wins', 'ball_recoveries', 'blocks', 'fouls_drawn', 'fouls_committed', 'yellow_cards', 'red_cards', 'saves']


#Para mostrar estadisticas
class ClubSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'logo']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url) if request else f"{settings.MEDIA_URL}{obj.logo.url}"
        return None

class MatchesByTournamentSerializer(serializers.ModelSerializer):
    home_team = ClubSerializer()
    away_team = ClubSerializer()

    class Meta:
        model = Match
        fields = ['id', 'tournament', 'home_team', 'away_team', 'round', 'date', 'score_home', 'score_away', 'state']


#Obtener estadisticas de clubes
class ClubStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubStatistics

    def to_representation(self, instance):
        return {
            'total_wins': instance.total_wins,
            'total_losses': instance.total_losses,
            'total_draws': instance.total_draws,
            'goals_scored': instance.goals_scored,
            'goals_conceded': instance.goals_conceded,
            'club': {
                'club_id': instance.participation.club.id,
                'club_name': instance.participation.club.name,
                'club_logo': self.context['request'].build_absolute_uri(instance.participation.club.logo.url) if instance.participation.club.logo else None
            }
        } 




