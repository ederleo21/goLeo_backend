from django.db.models.signals import post_save
from django.dispatch import receiver
from tournaments.models import Participation
from .models import ClubStatistics

@receiver(post_save, sender=Participation)
def create_club_statistics(sender, instance, created, **kwargs):
    
    if created:
        ClubStatistics.objects.create(participation=instance)


