from .models import Match
import logging

logger = logging.getLogger(__name__)

def generate_league_matches(tournament, is_single_round=True):
    teams = list(tournament.participants.values_list('club', flat=True))  
    num_teams = len(teams)

    if num_teams % 2 != 0:
        raise ValueError("El número de equipos debe ser par.")

    rounds = []
    for round_num in range(num_teams - 1):
        round_matches = []
        for i in range(num_teams // 2):
            home = teams[i]
            away = teams[-(i + 1)]
            round_matches.append((home, away))
        rounds.append(round_matches)

        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    if not is_single_round:
        reverse_rounds = []
        for round_matches in rounds:
            reverse_rounds.append([(away, home) for home, away in round_matches])
        rounds.extend(reverse_rounds)

    matches = []
    for round_num, round_matches in enumerate(rounds, start=1):
        for home_id, away_id in round_matches:
            match = Match(
                tournament=tournament,
                home_team_id=home_id,
                away_team_id=away_id,
                round=round_num  
            )
            matches.append(match)

    Match.objects.bulk_create(matches)


