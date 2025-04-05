from rest_framework import serializers
from core.models import Club, Player
from tournaments.models import Match, PlayerParticipation, Tournament, Participation
from tournaments.serializers.league_serializers import LeagueSerializer
from tournaments.serializers.cup_serializers import CupSerializer
from tournaments.utils import generate_league_matches

#Devolver torneos de cup y league, con campos dinamicos dependiente de torneo.
class ClubMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'logo']


class TournamentSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True)
    cup = CupSerializer(read_only=True)
    clubs = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'type', 'start_date', 'end_date', 'photo', 'active', 'description', 'league', 'cup', 'clubs']

    def get_clubs(self, instance):
        clubs = Club.objects.filter(id__in=instance.participants.values_list('club_id', flat=True))
        context = self.context  
        return ClubMinimalSerializer(clubs, many=True, context=context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.type == 'LEAGUE':
            data.pop('cup')
        elif instance.type == 'CUP':
            data.pop('league')
        elif instance.type == 'FRIENDLY':
            data.pop('cup')
            data.pop('league')
        return data


#Crear torneo general
class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name', 'type', 'start_date', 'end_date', 'photo', 'active', 'description']


#Devolver partidos  con informacion de sus clubes participantes
class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.SerializerMethodField(read_only=True)
    away_team_name = serializers.SerializerMethodField(read_only=True)
    home_team_logo = serializers.SerializerMethodField(read_only=True)
    away_team_logo = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Match
        fields = ['id', 'tournament', 'home_team', 'away_team', 'round', 'date', 'description', 'score_home', 'score_away', 'state', 'home_team_name', 'away_team_name', 'home_team_logo', 'away_team_logo']

    def get_home_team_name(self, obj):
        return obj.home_team.name  

    def get_away_team_name(self, obj):
        return obj.away_team.name 

    def get_home_team_logo(self, obj):
        if obj.home_team.logo: 
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.home_team.logo.url)
            return obj.home_team.logo.url
        return None

    def get_away_team_logo(self, obj):
        if obj.away_team.logo:  
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.away_team.logo.url)
            return obj.away_team.logo.url
        return None
    

#Serializer de modelo Participation
class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['tournament', 'club']


#Serializer para registrar equipos a un torneo.
class TournamentWithParticipantsSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()
    club_ids = serializers.ListField(child=serializers.IntegerField()) 

    def validate_tournament_id(self, value):
        if not Tournament.objects.filter(id=value).exists():
            raise serializers.ValidationError("El torneo con el ID proporcionado no existe")
        return value
    
    def validate_club_ids(self, value):
        if not value:
            raise serializers.ValidationError("La lista de clubes no puede estar vacía.")

        clubs = Club.objects.filter(id__in=value)
        if clubs.count() != len(value):
            raise serializers.ValidationError("Uno o más clubes no existen")

        return value

    def create(self, validated_data):
        tournament_id = validated_data['tournament_id']
        club_ids = validated_data['club_ids']

        tournament = Tournament.objects.get(id=tournament_id)

        participations = []
        for club_id in club_ids:
            club = Club.objects.get(id=club_id)

            if Participation.objects.filter(tournament=tournament, club=club).exists():
                raise serializers.ValidationError(f"El club con ID {club_id} ya está registrado en este torneo")

            participation = Participation.objects.create(tournament=tournament, club=club)
            participations.append(participation)

        if tournament.type == 'LEAGUE':
            league = tournament.league
            league.teams_count = len(club_ids)
            if league.league_format == 'SINGLE':
                league.rounds = league.teams_count - 1
                is_single_round = True
            elif league.league_format == 'DOUBLE':
                league.rounds = (league.teams_count - 1) * 2
                is_single_round = False
            league.save()

            generate_league_matches(tournament, is_single_round=is_single_round)

        if tournament.type == 'CUP':
            pass

        return participations


#Serializer de modelo PlayerParticipation
class PlayerParticipationSerializer(serializers.ModelSerializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())

    class Meta:
        model = PlayerParticipation
        fields = ['match', 'player']


#Devuelve la información de un partido, con su club y sus players participantes para hacer formulario y registrar -----------------------------------
class PlayersParticipationMatchSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField() 
    position = serializers.CharField(source='player.position.description', default="Sin posición")
    
    class Meta:
        model = PlayerParticipation
        fields = ['id', 'full_name', 'position', 'photo']

    def get_full_name(self, obj):
        return f"{obj.player.first_name} {obj.player.last_name}"

    def get_photo(self, obj):
        request = self.context.get('request')  
        if obj.player.photo: 
            return request.build_absolute_uri(obj.player.photo.url) if request else obj.player.photo.url
        return None 


class MatchWithPlayersGroupedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'date', 'state', 'score_home', 'score_away', 'home_team', 'away_team']

    def to_representation(self, instance):
        home_players = instance.participations_players.filter(player__club=instance.home_team)
        away_players = instance.participations_players.filter(player__club=instance.away_team)

        data = {
            "id": instance.id,
            "date": instance.date,
            "state": instance.state,
            "score_home": instance.score_home,
            "score_away": instance.score_away,
            "home_team": {
                "club_id": instance.home_team.id,
                "club_name": instance.home_team.name,
                "club_logo": self.context['request'].build_absolute_uri(instance.home_team.logo.url) if instance.home_team.logo else None,
                "players": PlayersParticipationMatchSerializer(home_players, many=True, context=self.context).data

            },
            "away_team": {
                "club_id": instance.away_team.id,
                "club_name": instance.away_team.name,
                "club_logo": self.context['request'].build_absolute_uri(instance.away_team.logo.url) if instance.away_team.logo else None,
                "players": PlayersParticipationMatchSerializer(away_players, many=True, context=self.context).data
            }
        }
        return data
#-------------------------------------------------------------------------------------------------------------------------------------------------

#Actualizar marcador de un partido
class MatchScoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['score_home', 'score_away']
        extra_kwargs = {'score_home': {'required': True}, 'score_away': {'required': True}}



















