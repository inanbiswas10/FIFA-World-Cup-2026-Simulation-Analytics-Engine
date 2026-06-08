import numpy as np
import pandas as pd
import json

class WorldCupKnockoutEngine:
    def __init__(self, ai_predictor):
        self.ai_predictor = ai_predictor

    def simulate_knockout_fixture (self,team_a,team_b):
        t1_feats = self.ai_predictor.get_team_features(team_a)
        t2_feats = self.ai_predictor.get_team_features(team_b)
        
        rank_diff = t1_feats["rank"] - t2_feats["rank"]
        squad_diff = t1_feats["squad_value"] - t2_feats["squad_value"]
        form_diff = t1_feats["form"] - t2_feats["form"]
        travel_fatigue = 0 
        
        match_vector = np.array([[rank_diff, squad_diff, form_diff, travel_fatigue]])
        scaled_vector = self.ai_predictor.scaler.transform(match_vector)
        
        prediction = self.ai_predictor.model.predict(scaled_vector)[0]
        
        if prediction == 2:    
            home_goals = int(np.random.choice([1, 2, 3], p=[0.5, 0.4, 0.1]))
            away_goals = int(np.random.choice([0, 1], p=[0.8, 0.2]))
            if home_goals <= away_goals: home_goals = away_goals + 1
            return team_a, f"{home_goals}-{away_goals}"
            
        elif prediction == 0:  
            away_goals = int(np.random.choice([1, 2, 3], p=[0.5, 0.4, 0.1]))
            home_goals = int(np.random.choice([0, 1], p=[0.8, 0.2]))
            if away_goals <= home_goals: away_goals = home_goals + 1
            return team_b, f"{home_goals}-{away_goals}"
            
        else:                 
            form_edge_team = team_a if t1_feats["form"] >= t2_feats["form"] else team_b
            tiebreaker_method = np.random.choice(["ET", "PEN"], p=[0.4, 0.6])
            
            ft_home_goals = int(np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2]))
            ft_away_goals = ft_home_goals
            
            if tiebreaker_method == "ET":
                if form_edge_team == team_a:
                    et_home_goals = ft_home_goals + 1
                    et_away_goals = ft_away_goals
                    winner = team_a
                else:
                    et_home_goals = ft_home_goals
                    et_away_goals = ft_away_goals + 1
                    winner = team_b
                    
                return winner, f"{et_home_goals}-{et_away_goals} (AET)"
            
            else:
                winner = np.random.choice([team_a, team_b], p=[0.5, 0.5])
                pk_w = 5 if np.random.rand() > 0.4 else 4
                pk_l = pk_w - int(np.random.choice([1, 2], p=[0.8, 0.2]))
                
                if winner == team_a:
                    return team_a, f"{ft_home_goals}-{ft_away_goals} (AET) ({pk_w}-{pk_l} PK)"
                else:
                    return team_b, f"{ft_home_goals}-{ft_away_goals} (AET) ({pk_l}-{pk_w} PK)"

    def run_knockout_stage(self, qualified_teams):
        current_round_teams = qualified_teams
        round_names = ["Round of 32", "Round of 16", "Quarter-finals", "Semi-finals", "Final"]
        
        # 📂 Storage nested dictionary for database collection
        tournament_history_db = {}
        
        for round_name in round_names:
            if len(current_round_teams) < 2:
                break
                
            print(f"\n🚀 FIFA World Cup 2026 {round_name} Prediction ({len(current_round_teams)} Teams) 🚀")
            next_round_teams = []
            round_matches_log = []
            
            w_home = 20
            w_vs = 6
            w_away = 20
            w_winner_team = 20
            
            for i in range(0, len(current_round_teams), 2):
                team_a = current_round_teams[i]
                team_b = current_round_teams[i+1]
                
                winner, score_detail = self.simulate_knockout_fixture(team_a, team_b)
                
                score_detail_expanded = score_detail.replace("(AET)", "After Extra Time")
                score_detail_expanded = score_detail_expanded.replace("PK)", "After Penalty Shootout)")
                
                str_matchup = f"{team_a:<{w_home}}{'vs':^{w_vs}}{team_b:>{w_away}}"
                str_result  = f"Winner: {winner:<{w_winner_team}} ({score_detail_expanded})"
                
                print(f"{str_matchup}    {str_result}")
                
                # Append individual map values into structural round logger array
                round_matches_log.append({
                    "home_team": team_a,
                    "away_team": team_b,
                    "winner": winner,
                    "scoreline": score_detail_expanded
                })
                next_round_teams.append(winner)
            
            tournament_history_db[round_name] = round_matches_log
            current_round_teams = next_round_teams
            
        champion_team = current_round_teams[0]
        tournament_history_db["Champions"] = champion_team

        print("\n" + "="*75)
        print(f"🏆👑 FIFA World Cup 2026 (USA,Canada,Mexico) Champions: {champion_team.upper()} 👑🏆")
        print("="*75 + "\n")
        
        with open("tournament_history.json", "w") as f:
            json.dump(tournament_history_db, f, indent=4)
        print("File Saved Successfully !! 'tournament_history.json' created in workspace root.")