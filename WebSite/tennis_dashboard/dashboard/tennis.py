import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from FinalModel.predictMatch import predict_match as model
from datetime import datetime


def calculate_age(birth_date, specific_date):
    birth_datetime = datetime.strptime(birth_date, "%Y-%m-%d")
    specific_datetime = datetime.strptime(specific_date, "%Y-%m-%d")
    age = specific_datetime.year - birth_datetime.year
    if (specific_datetime.month, specific_datetime.day) < (birth_datetime.month, birth_datetime.day):
        age -= 1
    return age


def predict(player1, player2, tournament, surface, round, player1_stats, player2_stats):
    data = {
        "Player": player1.name,
        "Opponent": player2.name,
        "Tournament": tournament.tournament,
        "Surface": surface,
        "Round": round,
        "Difference_in_ranks": abs(int(player1_stats.rank) - int(player2_stats.rank)),
        "Different_hand": [1 if player1.hand == player2.hand else 0],
        "Age": player1_stats.age,
        "Rank": player1_stats.rank,
        "Hand": 'L' if player1.hand == 'Left-Handed' else 'R',
        "Height": player1_stats.height,
        "Wins_semester": player1_stats.wins_semester,
        "Losses_semester": player1_stats.losses_semester,
        "Wins_year": player1_stats.wins_year,
        "Losses_year": player1_stats.losses_year,
        "Wins_clay": player1_stats.wins_clay,
        "Wins_hard": player1_stats.wins_hard,
        "Wins_grass": player1_stats.wins_grass,
        "Losses_clay": player1_stats.losses_clay,
        "Losses_hard": player1_stats.losses_hard,
        "Losses_grass": player1_stats.losses_grass,
        "Opponent_Age": player2_stats.age,
        "Opponent_Rank": player2_stats.rank,
        "Opponent_Hand": 'L' if player2.hand == 'Left-Handed' else 'R',
        "Opponent_Height": player2_stats.height,
        "Opponent_Wins_semester": player2_stats.wins_semester,
        "Opponent_Losses_semester": player2_stats.losses_semester,
        "Opponent_Wins_year": player2_stats.wins_year,
        "Opponent_Losses_year": player2_stats.losses_year,
        "Opponent_Wins_clay": player2_stats.wins_clay,
        "Opponent_Wins_hard": player2_stats.wins_hard,
        "Opponent_Wins_grass": player2_stats.wins_grass,
        "Opponent_Losses_clay": player2_stats.losses_clay,
        "Opponent_Losses_hard": player2_stats.losses_hard,
        "Opponent_Losses_grass": player2_stats.losses_grass
    }
    prediction = model(data)
    prediction_int = (prediction >= 0.5).astype(int)
    return prediction_int
