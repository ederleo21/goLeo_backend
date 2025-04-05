from rest_framework import generics
from ..models import Country
from ..serializers import CountrySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


