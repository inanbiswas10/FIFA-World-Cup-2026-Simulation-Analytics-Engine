import pandas as pd
import numpy as np
from pipeline import Tournament_Data_Pipeline
from simulator import MatchSimulator
from ml_engine import WorldCupMLPredictor
from knockout_engine import WorldCupKnockoutEngine

ai_predictor = WorldCupMLPredictor ()
ai_predictor.train_predictive_model ()

class World_Cup_Schedule_Engine:
    def __init__(self,fixtures_csv):
        self.fixtures_df = pd.read_csv (fixtures_csv)
        self.pipeline = Tournament_Data_Pipeline (fixtures_csv)
        self.simulator = MatchSimulator ()
        
        self.standings = {}
        print(f"🗓️  FIFA World Cup 2026 Schedule Engine Active: Loaded {len(self.fixtures_df)} Group Stage Fixtures With Stadium Vectors !!")
        print ("\n")

    def _initialize_team_standing (self,group,team):
        if group not in self.standings:
            self.standings [group] = {}
        if team not in self.standings [group]:
            self.standings [group][team] = {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}

    def process_all_group_fixtures (self):
        print("\n⚡ Generating Operational Projections For FIFA World Cup 2026 Group Stage Fixtures !!")
        print ("\n")
        calculated_fixtures = []

        for index, row in self.fixtures_df.iterrows ():
            group = row ["group"]
            date = row ["date"]
            time_ist = row ["time_ist"]
            team_a = row ["home_team"]
            team_b = row ["away_team"]
            venue = row ["venue"]
            
            self._initialize_team_standing (group,team_a)
            self._initialize_team_standing (group,team_b)
            
            try:
                t1_feats = ai_predictor.get_team_features (team_a)
                t2_feats = ai_predictor.get_team_features (team_b)
                
                rank_diff = t1_feats ["rank"]-t2_feats ["rank"]
                squad_diff = t1_feats ["squad_value"]-t2_feats ["squad_value"]
                form_diff = t1_feats ["form"]-t2_feats ["form"]
                travel_fatigue = 0 
                
                match_vector = np.array ([[rank_diff,squad_diff,form_diff,travel_fatigue]])
                scaled_vector = ai_predictor.scaler.transform (match_vector)
                
                prediction = ai_predictor.model.predict (scaled_vector) [0]
                
                home_goals,away_goals = 0,0
                if prediction == 2:   
                    home_goals = int (np.random.choice ([1,2,3],p = [0.4,0.4,0.2]))
                    away_goals = int (np.random.choice ([0,1],p = [0.7,0.3]))
                    if home_goals <= away_goals: home_goals = away_goals + 1
                elif prediction == 0:  
                    away_goals = int (np.random.choice ([1,2,3],p = [0.4,0.4,0.2]))
                    home_goals = int (np.random.choice ([0,1],p = [0.7,0.3]))
                    if away_goals <= home_goals: away_goals = home_goals + 1
                else:                 
                    home_goals = int (np.random.choice ([0,1,2],p = [0.3,0.5,0.2]))
                    away_goals = home_goals

                stats_a = self.standings [group][team_a]
                stats_b = self.standings [group][team_b]
                
                stats_a ["P"] += 1; stats_b ["P"] += 1
                stats_a ["GF"] += home_goals; stats_a ["GA"] += away_goals
                stats_b ["GF"] += away_goals; stats_b ["GA"] += home_goals
                
                if home_goals > away_goals:
                    stats_a ["W"] += 1; stats_a ["Pts"] += 3
                    stats_b ["L"] += 1
                elif away_goals > home_goals:
                    stats_b ["W"] += 1; stats_b ["Pts"] += 3
                    stats_a ["L"] += 1
                else:
                    stats_a ["D"] += 1; stats_a ["Pts"] += 1
                    stats_b ["D"] += 1; stats_b ["Pts"] += 1
                    
                stats_a ["GD"] = stats_a ["GF"] - stats_a ["GA"]
                stats_b ["GD"] = stats_b ["GF"] - stats_b ["GA"]

                calculated_fixtures.append ({
                    "Group": group,
                    "Kickoff (IST)": f"{date} (2026),{time_ist}",
                    "Fixtures": f"{team_a} vs {team_b}",
                    "Full Time Score": f"{team_a} {home_goals}-{away_goals} {team_b}",
                    "Venue": venue
                })
            except ValueError as e:
                print(f"⚠️ Data Mismatch Row {index}: {e}")
                continue

        return pd.DataFrame (calculated_fixtures)

    def print_final_group_tables (self):
        print ("\n🏆 FIFA World Cup 2026 Final Group Stage Standings 🏆")
        for group, teams in sorted (self.standings.items ()):
            print (f"\n🔹 Group {group} 🔹")
            print (f"{'Teams':<25}{'P':^4}{'W':^4}{'D':^4}{'L':^4}{'GF':^4}{'GA':^4}{'GD':^4}{'Pts':^5}")
            print ("-" * 62)
            
            sorted_teams = sorted (
                teams.items (), 
                key = lambda item: (item [1]["Pts"],item [1]["GD"],item [1]["GF"]), 
                reverse = True
            )
            
            for team, stats in sorted_teams:
                print (f"{team:<25}{stats ['P']:^4}{stats ['W']:^4}{stats ['D']:^4}{stats ['L']:^4}{stats ['GF']:^4}{stats ['GA']:^4}{stats ['GD']:^4}{stats ['Pts']:^5}")

    def extract_group_qualifiers (self):
        print("\n🎟️  Processing FIFA World Cup 2026 Tournament Advancement Vector !!")
        automatic_qualifiers = []
        
        for group, teams in sorted (self.standings.items ()):
            sorted_teams = sorted (
                teams.items (), 
                key = lambda item: (item [1]["Pts"],item [1]["GD"],item [1]["GF"]), 
                reverse = True
            )
            
            winner = sorted_teams [0][0]
            runner_up = sorted_teams [1][0]
            
            automatic_qualifiers.append ({"Group": group, "Team": winner, "Position": "1st (Group Winner)"})
            automatic_qualifiers.append ({"Group": group, "Team": runner_up, "Position": "2nd (Group Runner-Up)"})
            
        return automatic_qualifiers
    
    def extract_best_third_place_qualifiers (self):

        all_third_place_teams = []
        
        for group,teams in self.standings.items ():
            sorted_teams = sorted (
                teams.items (), 
                key = lambda item: (item [1]["Pts"],item [1]["GD"],item [1]["GF"]), 
                reverse = True
            )
            team_name,stats = sorted_teams [2]
            all_third_place_teams.append ({
                "Group": str (group).strip (),
                "Team": str (team_name).strip (),  
                "Pts": stats ["Pts"],
                "GD": stats ["GD"],
                "GF": stats ["GF"]
            })
            
        global_third_place_ranking = sorted (
            all_third_place_teams,
            key = lambda x: (x ["Pts"],x ["GD"],x["GF"]),
            reverse = True
        )
        
        best_8_wildcards = global_third_place_ranking[:8]

        w_rank = 8
        w_group = 10
        w_team = 25
        w_pts = 8
        w_gd = 8
        w_gf = 8
        
        print ("\n🚀 FIFA World Cup 2026 Best 3rd Place Teams Qualification Scenario (Round Of 32) 🚀")
        
        headers = (
            f"{'Rank':^{w_rank}}"
            f"{'Group':^{w_group}}"
            f"{'Team':^{w_team}}"
            f"{'Pts':^{w_pts}}"
            f"{'GD':^{w_gd}}"
            f"{'GF':^{w_gf}}"
        )
        print (headers)
        print ("-" * len (headers))
        
        for idx,team_data in enumerate (best_8_wildcards,1):
            val_rank = f"{idx}"
            val_group = f"{team_data ['Group']}"
            val_team = f"{team_data ['Team']}"
            val_pts = f"{team_data ['Pts']}"
            val_gd = f"{team_data ['GD']}"
            val_gf = f"{team_data ['GF']}"

            row_str = (
                f"{val_rank:^{w_rank}}"
                f"{val_group:^{w_group}}"
                f"{val_team:^{w_team}}"
                f"{val_pts:^{w_pts}}"
                f"{val_gd:^{w_gd}}"
                f"{val_gf:^{w_gf}}"
            )
            print (row_str)
            
        return best_8_wildcards


if __name__ == "__main__":
    engine = World_Cup_Schedule_Engine ("fixtures.csv")
    results = engine.process_all_group_fixtures ()
    
    print("\n📋 Ingestion Sample Preview (Expanded Features): \n")
     
    padding = 6
    w_group = max (results ["Group"].astype (str).map (len).max (),len ("Group")) + padding
    w_kickoff = max (results ["Kickoff (IST)"].astype (str).map (len).max (),len ("Kickoff (IST)")) + padding
    w_matchup = max (results ["Fixtures"].astype (str).map (len).max (),len ("Fixtures")) + padding
    w_result = max (results ["Full Time Score"].astype (str).map (len).max (),len ("Full Time Score")) + padding
    w_venue = max(results ["Venue"].astype (str).map (len).max (),len ("Venue")) + padding
    
    headers = (
        f"{'Group':^{w_group}}"
        f"{'Kickoff (IST)':^{w_kickoff}}"
        f"{'Fixtures':^{w_matchup}}"
        f"{'Full Time Score':^{w_result}}"
        f"{'Venue':^{w_venue}}"
    )
    
    print (headers)
    print ()
    
    previous_group = None
    for _, row in results.iterrows ():
        current_group = str (row ['Group']).strip ()
        if previous_group is not None and current_group != previous_group:
            print ()
        previous_group = current_group

        row_str = (
            f"{str (row ['Group']):^{w_group}}"
            f"{str (row ['Kickoff (IST)']):^{w_kickoff}}"
            f"{str (row ['Fixtures']):^{w_matchup}}"
            f"{str (row ['Full Time Score']):^{w_result}}"
            f"{str (row ['Venue']):^{w_venue}}"
        )
        print (row_str)
        
    engine.print_final_group_tables ()
    qualifiers = engine.extract_group_qualifiers ()

    print("\n🚀 FIFA World Cup 2026 Round Of 32 Qualification Scenario 🚀")
    print(f"{'Group':^10}{'Qualified Teams':<25}{'Current Status':<15}")
    print("-" * 55)
    
    previous_q_group = None
    for team_data in qualifiers:
        current_q_group = str (team_data ['Group']).strip ()
        if previous_q_group is not None and current_q_group != previous_q_group:
            print ()
            
        previous_q_group = current_q_group
        print (f"{team_data ['Group']:^10}{team_data ['Team']:<25}{team_data ['Position']:<15}")

    flat_qualified_teams = [team_dict ["Team"] for team_dict in qualifiers]
    
    third_place_wildcards = engine.extract_best_third_place_qualifiers ()
    flat_wildcards = [team_dict ["Team"] for team_dict in third_place_wildcards]
    
    full_round_of_32_field = flat_qualified_teams + flat_wildcards
    knockout_simulator = WorldCupKnockoutEngine (ai_predictor)
    knockout_simulator.run_knockout_stage (full_round_of_32_field)

    print ("\n📊 FIFA World Cup 2026 Tournament Simulation Engine Machine Learning Model Insights (Random Forest) 📊")
    
    importances = ai_predictor.model.feature_importances_
    feature_names = ["FIFA Ranking Differential","Squad Value Differential","Form Rating Differential","Travel Fatigue"]
    
    print (f"{'Input Feature Name':<30}{'Weight/Relative Importance':^30}")
    print ("-" * 60)
    
    for name, importance in zip (feature_names,importances):
        percentage_str = f"{importance*100:.2f} %"
        print (f"{name:<30}{percentage_str:^30}")
    print ("-" * 60 + "\n")