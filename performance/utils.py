from django.db import transaction
from .models import ClubStatistics, Participation

def update_club_statistics(match, previous_score_home, previous_score_away):
    with transaction.atomic():
        try:
            participation_home = Participation.objects.get(club=match.home_team, tournament=match.tournament)
            participation_away = Participation.objects.get(club=match.away_team, tournament=match.tournament)
        except Participation.DoesNotExist:
            return 
        
        home_stats, _ = ClubStatistics.objects.get_or_create(participation=participation_home)
        away_stats, _ = ClubStatistics.objects.get_or_create(participation=participation_away)

        if match.state == "COMPLETED":
            if previous_score_home is not None and previous_score_away is not None:
                if previous_score_home > previous_score_away:
                    home_stats.total_wins -= 1
                    away_stats.total_losses -= 1
                elif previous_score_home < previous_score_away:
                    home_stats.total_losses -= 1
                    away_stats.total_wins -= 1
                else:
                    home_stats.total_draws -= 1
                    away_stats.total_draws -= 1

                home_stats.goals_scored -= previous_score_home
                home_stats.goals_conceded -= previous_score_away
                away_stats.goals_scored -= previous_score_away
                away_stats.goals_conceded -= previous_score_home

        if match.score_home > match.score_away:
            home_stats.total_wins += 1
            away_stats.total_losses += 1
        elif match.score_home < match.score_away:
            home_stats.total_losses += 1
            away_stats.total_wins += 1
        else:
            home_stats.total_draws += 1
            away_stats.total_draws += 1

        home_stats.goals_scored += match.score_home
        home_stats.goals_conceded += match.score_away
        away_stats.goals_scored += match.score_away
        away_stats.goals_conceded += match.score_home

        home_stats.save()
        away_stats.save()




