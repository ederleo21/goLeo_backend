from rest_framework import generics, status
from ..models import Club
from ..serializers import ClubSerializer, ClubCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response 

#Obtener todos los clubes disponibles
class ClubListView(generics.ListAPIView):
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Club.objects.all()
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')
        return queryset

#Crear un club
class ClubCreateView(generics.CreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubCreateSerializer
    permission_classes = [IsAuthenticated]


#Obtener los detalles de un club especifico
class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]


#Actualizar un club existente
class ClubUpdateView(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubCreateSerializer
    permission_classes = [IsAuthenticated]


#Eliminar un club
class ClubDeleteView(generics.DestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]


