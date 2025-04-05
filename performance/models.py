from django.db import models
from django.forms import ValidationError
from tournaments.models import Participation, PlayerParticipation

class ClubStatistics(models.Model):
    participation = models.OneToOneField(Participation, on_delete=models.CASCADE, verbose_name="Participación de club en torneo", related_name="statistics")
    total_wins = models.PositiveIntegerField(verbose_name="Partidos ganados", default=0)
    total_losses = models.PositiveIntegerField(verbose_name="Partidos perdidos", default=0)
    total_draws = models.PositiveIntegerField(verbose_name="Partidos empatados", default=0)
    goals_scored = models.PositiveIntegerField(verbose_name="Goles marcados", default=0)
    goals_conceded = models.PositiveIntegerField(verbose_name="Goles recibidos", default=0)

    class Meta:
        verbose_name = "Estadisticas de Club"
        verbose_name_plural = "Estadisticas de Clubes"
    
    def __str__(self):
        return f"Estadísticas de {self.participation.club.name} en {self.participation.tournament.name}"


class PlayerStatistics(models.Model):
    player_participation = models.OneToOneField(PlayerParticipation, verbose_name="Participacion de jugador en partido", on_delete=models.CASCADE, related_name="statistics")
    goals_scored = models.PositiveIntegerField(verbose_name="Goles marcados", default=0)
    assists = models.PositiveIntegerField(verbose_name="Asistencias", default=0)
    shots_on_target = models.PositiveIntegerField(verbose_name="Tiros al arco", default=0)
    completed_passes = models.PositiveIntegerField(verbose_name="Pases completados", default=0)
    duel_wins = models.PositiveIntegerField(verbose_name="Duelos ganados", default=0)
    ball_recoveries = models.PositiveIntegerField(verbose_name="Recuperaciones de balon", default=0)
    blocks = models.PositiveIntegerField(verbose_name="Bloqueos", default=0)
    fouls_drawn = models.PositiveIntegerField(verbose_name="Faltas recibidas", default=0)
    fouls_committed = models.PositiveIntegerField(verbose_name="Faltas cometidas", default=0)
    yellow_cards = models.PositiveIntegerField("Tarjetas amarillas", default=0)
    red_cards = models.PositiveIntegerField(verbose_name="Tarjetas rojas", default=0)
    saves = models.PositiveIntegerField(verbose_name="Atajadas", default=0)

    class Meta:
        verbose_name = 'Estadísticas de Jugador'
        verbose_name_plural = 'Estadísticas de Jugadores'

    def __str__(self):
        return f"Estadísticas de {self.player_participation.player.first_name} en {self.player_participation.match}"




