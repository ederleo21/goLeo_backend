from django.contrib import admin
from .models import ClubStatistics, PlayerStatistics

admin.site.register([ClubStatistics, PlayerStatistics])
