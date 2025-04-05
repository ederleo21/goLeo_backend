from rest_framework import generics
from ..models import Position
from ..serializers import PositionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class PositionListView(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]















