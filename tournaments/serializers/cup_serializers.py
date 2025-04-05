from rest_framework import serializers
from tournaments.models import Cup, Tournament

#Serializer modelo Cup
class CupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cup
        fields = ['stages']


#Crear torneo tipo Copa
class CreateCupSerializer(serializers.ModelSerializer):
    tournament_id = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all(), source='tournament')

    class Meta:
        model = Cup
        fields = ['tournament_id', 'stages']



