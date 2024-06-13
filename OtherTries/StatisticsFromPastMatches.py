import pandas as pd

# Example DataFrame structure for past matches
past_matches = pd.DataFrame({
    'player': ['Player A', 'Player A', 'Player A', 'Player B', 'Player B', 'Player B'],
    'opponent': ['Player X', 'Player Y', 'Player Z', 'Player X', 'Player Y', 'Player Z'],
    'surface': ['hard', 'clay', 'grass', 'hard', 'clay', 'grass'],
    'first_serve_pct': [65, 60, 70, 62, 58, 66],
    'aces': [10, 8, 12, 9, 7, 11],
    'double_faults': [2, 3, 1, 3, 4, 2],
    'first_serve_points_won': [70, 68, 72, 68, 65, 70],
    'second_serve_points_won': [50, 48, 52, 49, 47, 51],
    'break_points_saved': [75, 72, 78, 73, 70, 76],
    'return_points_won': [40, 38, 42, 39, 37, 41],
    'break_points_converted': [30, 28, 32, 29, 27, 31]
})

# Filter numeric columns only
numeric_columns = ['first_serve_pct', 'aces', 'double_faults', 'first_serve_points_won',
                   'second_serve_points_won', 'break_points_saved', 'return_points_won', 'break_points_converted']

# Overall averages for Player A and Player B
player_a_stats = past_matches[past_matches['player'] == 'Player A'][numeric_columns].mean()
player_b_stats = past_matches[past_matches['player'] == 'Player B'][numeric_columns].mean()

surface = 'hard'  # Assuming the upcoming match is on a hard court

player_a_surface_stats = past_matches[(past_matches['player'] == 'Player A') & (past_matches['surface'] == surface)][
    numeric_columns].mean()
player_b_surface_stats = past_matches[(past_matches['player'] == 'Player B') & (past_matches['surface'] == surface)][
    numeric_columns].mean()

# Assuming we have head-to-head data
head_to_head_matches = pd.DataFrame({
    'player': ['Player A', 'Player B'],
    'opponent': ['Player B', 'Player A'],
    'first_serve_pct': [63, 61],
    'aces': [11, 10],
    'double_faults': [2, 3],
    'first_serve_points_won': [69, 67],
    'second_serve_points_won': [51, 49],
    'break_points_saved': [74, 72],
    'return_points_won': [41, 39],
    'break_points_converted': [31, 29]
})

player_a_h2h_stats = head_to_head_matches[head_to_head_matches['player'] == 'Player A'][numeric_columns].mean()
player_b_h2h_stats = head_to_head_matches[head_to_head_matches['player'] == 'Player B'][numeric_columns].mean()

weights = {
    'overall': 0.4,
    'surface': 0.3,
    'head_to_head': 0.3
}


def weighted_average(player_stats, surface_stats, h2h_stats, weights):
    combined_stats = {}
    for stat in player_stats.index:
        combined_stats[stat] = (
                player_stats[stat] * weights['overall'] +
                surface_stats[stat] * weights['surface'] +
                h2h_stats[stat] * weights['head_to_head']
        )
    return combined_stats


player_a_combined_stats = weighted_average(player_a_stats, player_a_surface_stats, player_a_h2h_stats, weights)
player_b_combined_stats = weighted_average(player_b_stats, player_b_surface_stats, player_b_h2h_stats, weights)

print("Player A Combined Statistics:")
print(player_a_combined_stats)

print("Player B Combined Statistics:")
print(player_b_combined_stats)
