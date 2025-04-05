from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import League, Cup

@receiver(post_delete, sender=League)
def delete_related_tournament(sender, instance, **kwargs):

    if instance.tournament:
        instance.tournament.delete()

@receiver(post_delete, sender=Cup)
def delete_related_tournament(sender, instance, **kwargs):

    if instance.tournament:
        instance.tournament.delete()


