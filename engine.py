import numpy as np
from scipy.stats import poisson

def calculate_match_probabilities (home_expected_goals,away_expected_goals,max_goals = 6):

  home_probabilities = [poisson.pmf (i,home_expected_goals) for i in range (max_goals)]
  away_probabilities = [poisson.pmf (i,away_expected_goals) for i in range (max_goals)]

  probability_matrix = np.outer (home_probabilities,away_probabilities)

  draw_probability = np.sum (np.diag (probability_matrix))
  home_win_probability = np.sum (np.tril (probability_matrix,-1))
  away_win_probability = np.sum (np.triu (probability_matrix,1))

  return {
    "home_win": float (home_win_probability),
    "away_win": float (away_win_probability),
    "draw": float (draw_probability),
    "raw_matrix": probability_matrix
  }

if __name__ == "__main__":
  print ("⚽ Initializing FIFA World Cup 2026 Match Prediction Engine...")
  
  home_team = "Brazil"
  away_team = "Morocco"

  brazil_exp_goals = 2.2
  morocco_exp_goals = 1.1

  results = calculate_match_probabilities (brazil_exp_goals,morocco_exp_goals)

  print (f"\n🏆 FIFA World Cup 2026 Group C Match Simulation: {home_team} vs {away_team}")
  print ("-"*70)
  print (f"🇧🇷 {home_team} Win Probability : {results ['home_win']*100:.2f}%")
  print (f"🇲🇦 {away_team} Win Probability : {results ['away_win']*100:.2f}%")
  print (f"🤝 Draw Probability           : {results ['draw']*100:.2f}%")
  print ("-"*70)

  matrix = results ['raw_matrix']

  best_score_indices = np.unravel_index (np.argmax (matrix),matrix.shape)
  highest_prob = matrix [best_score_indices]*100

  print (f"🔥 Most Likely Full Time Score: {home_team} {best_score_indices [0]} - {best_score_indices [1]} {away_team}")
  print (f"📈 Probability of this exact outcome: {highest_prob:.2f}%")


