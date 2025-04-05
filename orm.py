import os
import django
from django.db.models import Count, Min, Max, Avg, Sum, F, Q
from django.shortcuts import get_object_or_404
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "club_project.settings")
django.setup()
from core.models import Player, Club, Country, PlayerSkill
from tournaments.models import Tournament, Participation, PlayerParticipation, Match
from performance.models import ClubStatistics, PlayerStatistics


speed_stats = PlayerSkill.objects.aggregate(max_speed=Max('speed'), min_speed=Min('speed'))
print(speed_stats)






