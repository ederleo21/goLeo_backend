from django.db import models
from django.utils import timezone
from core.models import Club, Player
from django.core.exceptions import ValidationError

class Tournament(models.Model):
    TOURNAMENTS_TYPES = [
        ('LEAGUE', 'Liga'),
        ('CUP', 'Copa'),
        ('FRIENDLY', 'Amistoso'),
        ('OTHER', 'Otro')
    ]

    name = models.CharField(verbose_name="Nombre" ,max_length=100, unique=True)
    type = models.CharField(verbose_name="Tipo", max_length=10, choices=TOURNAMENTS_TYPES, default='OTHER')
    start_date = models.DateField(verbose_name="Fecha de inicio", default=timezone.now)
    end_date = models.DateField(verbose_name="Fecha de fin")
    photo = models.ImageField(verbose_name='Foto del torneo', upload_to='tournaments/', default='tournaments/tournament_default.jpg', blank=True, null=True)
    active = models.BooleanField(verbose_name="Activo", default=True)
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
   
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class League(models.Model):

    LEAGUE_FORMATS = [
        ('SINGLE', 'Solo ida'),
        ('DOUBLE', 'Ida y vuelta')
    ]

    tournament = models.OneToOneField(Tournament, verbose_name="Torneo", on_delete=models.CASCADE, related_name="league")
    rounds = models.PositiveIntegerField(verbose_name="Jornadas", default=1, editable=False)
    points_system = models.JSONField(default=dict)
    league_format = models.CharField(verbose_name="Formato de liga", max_length=10, choices=LEAGUE_FORMATS, default='SINGLE')
    teams_count = models.PositiveIntegerField(verbose_name="Cantidad de equipos", default=0, editable=False)

    class Meta:
        verbose_name = 'Torneo Liga'
        verbose_name_plural = 'Torneos Ligas'

    def __str__(self):
        return f"Liga: {self.tournament.name}"

    def save(self, *args, **kwargs):
        if self.pk: 
            original = League.objects.get(pk=self.pk)
            
            if self.points_system != original.points_system:
                raise ValidationError("No se puede modificar el sistema de puntos después de creado el torneo.")
            if self.league_format != original.league_format:
                raise ValidationError("No se puede modificar el formato de liga después de creado el torneo.")
            if self.tournament_id != original.tournament_id:
                raise ValidationError("No se puede cambiar el torneo relacionado después de creado.")
        super().save(*args, **kwargs)


class Cup(models.Model):
    tournament = models.OneToOneField(Tournament, verbose_name="Torneo", on_delete=models.CASCADE, related_name="cup")    
    stages = models.PositiveIntegerField(verbose_name="Rondas", default=1)

    class Meta:
        verbose_name = 'Torneo Copa'
        verbose_name_plural = 'Torneos Copas'

    def __str__(self):
        return f"Copa: {self.tournament.name}"

    def delete(self, *args, **kwargs):
        if self.tournament:
            self.tournament.delete()
        super().delete(*args, **kwargs)


class Participation(models.Model):
    tournament = models.ForeignKey(Tournament, verbose_name="Torneo", on_delete=models.CASCADE, related_name="participants")
    club = models.ForeignKey(Club, verbose_name="Club", on_delete=models.PROTECT, related_name="tournaments")

    class Meta:
        verbose_name = 'Participación'
        verbose_name_plural = 'Participaciones'
        unique_together = ('tournament', 'club')

    def __str__(self):
        return f"{self.club.name} en {self.tournament.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:  
            raise ValidationError("No se permite modificar un registro de participación existente.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("No se permite eliminar un registro de participación directamente.")


class Match(models.Model):
    STATE_MATCH = [
        ('WAITING', 'Pendiente'),
        ('IN_PROGRESS', "En curso"),
        ('COMPLETED', "Completado")
    ]

    tournament = models.ForeignKey(Tournament, verbose_name="Torneo", on_delete=models.CASCADE, related_name="matches")
    home_team = models.ForeignKey(Club, verbose_name="Equipo local", on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(Club, verbose_name="Equipo visitante", on_delete=models.CASCADE, related_name="away_matches")
    round = models.PositiveIntegerField(verbose_name="Jornada", default=0, editable=False)
    date = models.DateField(verbose_name="Fecha", blank=True, null=True)
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)
    score_home = models.PositiveIntegerField(verbose_name="Goles de equipo local", null=True, blank=True, default=0)
    score_away = models.PositiveIntegerField(verbose_name="Goles de equipo visitante", null=True, blank=True, default=0)
    state = models.CharField(verbose_name="Estado", max_length=20, choices=STATE_MATCH, default='WAITING')

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} ({self.tournament.name})"

    def clean(self):
        if self.home_team == self.away_team:
            raise ValidationError("El equipo local no puede ser el mismo que el equipo visitante.")


class PlayerParticipation(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='participations_players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Jugador en partido'
        verbose_name_plural = 'Jugadores en partidos'

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} en {self.match}"


