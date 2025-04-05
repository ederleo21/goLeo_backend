from rest_framework import serializers
from .models import Club, Player, PlayerSkill, Country, Position
from django.contrib.auth import get_user_model

#Country serializers
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'flag']

#Clubs serializers
class ClubSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Club
        fields = '__all__'


class ClubCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = '__all__'

#Position serializers
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'description']

#Players serializers
class PlayerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSkill
        fields = ['passing', 'shooting', 'dribbling', 'defense', 'physical', 'speed', 'vision', 'goalkeeping']

#Se serializa y se anida la instancia del club, pais, skills y posicion del jugador
class PlayerSerializer(serializers.ModelSerializer):
    club = ClubSerializer()  
    nationality = CountrySerializer()
    position = PositionSerializer()
    skills = PlayerSkillSerializer()
  
    class Meta:
        model = Player
        fields = '__all__'

#Seralizer para crear y actualizar jugador
class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

#Serializer para crear y actualizar habilidades de jugador
class PlayerSkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSkill
        fields = '__all__'


#Users
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'dni', 'phone','address', 'image']

