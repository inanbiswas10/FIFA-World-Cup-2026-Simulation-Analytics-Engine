import pandas as pd
from pipeline import Tournament_Data_Pipeline
from simulator import MatchSimulator

class World_Cup_Schedule_Engine:
    def __init__(self,fixtures_csv):
        self.fixtures_df = pd.read_csv (fixtures_csv)
        self.pipeline = Tournament_Data_Pipeline (fixtures_csv)
        self.simulator = MatchSimulator ()
        
        self.standings = {}
        
        print (f"🗓️  FIFA World Cup 2026 Schedule Engine Active: Loaded {len (self.fixtures_df)} Group Stage Fixtures With Stadium Vectors !!")

    def _initialize_team_standing (self,group,team):
        if group not in self.standings:
            self.standings [group] = {}
        if team not in self.standings [group]:
            self.standings [group][team] = {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}

    def process_all_group_fixtures (self):
        print ("\n⚡ Generating Operational Projections For FIFA World Cup 2026 Group Stage Fixtures !!")
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
                lambda_a, lambda_b = self.pipeline.calculate_match_lambdas (team_a,team_b)
                home_goals, away_goals, points_a, points_b = self.simulator.simulate_match (lambda_a,lambda_b)
                
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

        print("\n🏆 FIFA World Cup 2026 Final Group Stage Standings 🏆")
        
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

        print ("\n🎟️  Processing FIFA World Cup 2026 Tournament Advancement Vector !!")
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


if __name__ == "__main__":
    engine = World_Cup_Schedule_Engine ("fixtures.csv")
    results = engine.process_all_group_fixtures ()
    
    print ("\n📋 Ingestion Sample Preview (Expanded Features): \n")
     
    padding = 6
    w_group = max (results ["Group"].astype (str).map (len).max (), len ("Group")) + padding
    w_kickoff = max (results ["Kickoff (IST)"].astype (str).map (len).max (), len ("Kickoff (IST)")) + padding
    w_matchup = max (results ["Fixtures"].astype (str).map (len).max (), len ("Fixtures")) + padding
    w_result = max (results ["Full Time Score"].astype (str).map (len).max (), len ("Full Time Score")) + padding
    w_venue = max (results ["Venue"].astype (str).map (len).max (), len ("Venue")) + padding
    
    headers = (
        f"{'Group':^{w_group}}"
        f"{'Kickoff (IST)':^{w_kickoff}}"
        f"{'Fixtures':^{w_matchup}}"
        f"{'Full Time Score':^{w_result}}"
        f"{'Venue':^{w_venue}}"
    )
    
    print(headers)
    print()
    
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

    print ("\n🚀 FIFA World Cup 2026 Round Of 32 Qualification Scenario 🚀")
    print (f"{'Group':^10}{'Qualified Team':<25}{'Current Status':<15}")
    print ("-" * 55)
    
    previous_q_group = None
    for team_data in qualifiers:
        current_q_group = str (team_data ['Group']).strip ()
        
        if previous_q_group is not None and current_q_group != previous_q_group:
            print ()
            
        previous_q_group = current_q_group
        print (f"{team_data ['Group']:^10}{team_data ['Team']:<25}{team_data ['Position']:<15}")
