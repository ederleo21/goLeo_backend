from rest_framework.response import Response 
from rest_framework import generics, status
from ..models import Player, PlayerSkill
from ..serializers import PlayerSerializer, PlayerCreateSerializer, PlayerSkillCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

logger = logging.getLogger(__name__)

#Obtener todos los jugadores o los jugadores de un club especifico
class PlayerListView(generics.ListAPIView):
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        club_id = self.request.query_params.get('club')
        active = self.request.query_params.get('active')

        queryset = Player.objects.all()

        if club_id:
            queryset = Player.objects.filter(club_id=club_id)

        if active is not None:
            active = active.lower() in ['true', '1', 't', 'y', 'yes']
            queryset = queryset.filter(active=active)

        return queryset

#Crear jugador
class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

#Crear habilidades de de un jugador creado
class PlayerSkillCreateView(generics.CreateAPIView):
    queryset = PlayerSkill.objects.all()
    serializer_class = PlayerSkillCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        player_id = request.data.get('player')
        if not player_id:
            return Response({"error": "Player ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(player=player)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Actualizar información personal de jugador
class PlayerUpdateView(generics.UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#Actualizar skills de un jugador
class PlayerSkillUpdateView(generics.UpdateAPIView):
    queryset = PlayerSkill.objects.all()
    serializer_class = PlayerSkillCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'player__id'
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

#Eliminar jugador
class PlayerDeleteView(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]


#Devolver un jugador especifico
class PlayerDetailView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'








