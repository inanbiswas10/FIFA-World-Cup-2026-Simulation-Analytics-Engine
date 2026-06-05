import pandas as pd
from pipeline import Tournament_Data_Pipeline
from simulator import MatchSimulator

class World_Cup_Schedule_Engine:
    def __init__(self,fixtures_csv):
        self.fixtures_df = pd.read_csv (fixtures_csv)
        self.pipeline = Tournament_Data_Pipeline (fixtures_csv)
        self.simulator = MatchSimulator ()
        print(f"🗓️  FIFA World Cup 2026 Schedule Engine Active: Loaded {len (self.fixtures_df)} Group Stage Fixtures With Stadium Vectors !!")

    def process_all_group_fixtures (self):
        print ("\n⚡ Generating Operational Projections For FIFA World Cup 2026 Group Stage Fixtures !!")
        calculated_fixtures = []

        for index,row in self.fixtures_df.iterrows ():
            group = row ["group"]
            date = row ["date"]
            time_ist = row ["time_ist"]
            team_a = row ["home_team"]
            team_b = row ["away_team"]
            venue = row ["venue"]
            
            try:
                lambda_a,lambda_b = self.pipeline.calculate_match_lambdas (team_a,team_b)
                home_goals,away_goals,points_a,points_b = self.simulator.simulate_match (lambda_a,lambda_b)
                
                calculated_fixtures.append ({
                    "Group": group,
                    "Kickoff (IST)": f"{date} (2026),{time_ist}",
                    "Fixtures": f"{team_a} vs {team_b}",
                    "Full Time Score": f"{team_a} {home_goals}-{away_goals} {team_b}",
                    "Venue": venue
                })
            except ValueError as e:
                print (f"⚠️ Data Mismatch Row {index}: {e}")
                continue

        return pd.DataFrame (calculated_fixtures)

if __name__ == "__main__":
    engine = World_Cup_Schedule_Engine ("fixtures.csv")
    results = engine.process_all_group_fixtures ()
    
    print ("\n📋 Ingestion Sample Preview (Expanded Features): \n")
    
    padding = 6
    
    w_group = max (results ["Group"].astype (str).map (len).max (),len ("Group")) + padding
    w_kickoff = max (results ["Kickoff (IST)"].astype (str).map (len).max (),len ("Kickoff (IST)")) + padding
    w_matchup = max (results ["Fixtures"].astype (str).map (len).max (),len ("Fixtures")) + padding
    w_result = max (results ["Full Time Score"].astype (str).map (len).max (),len ("Full Time Score")) + padding
    w_venue = max (results ["Venue"].astype (str).map (len).max (),len ("Venue")) + padding
    
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
            f"{ str (row ['Group']):^{w_group}}"
            f"{str (row ['Kickoff (IST)']):^{w_kickoff}}"
            f"{str (row ['Fixtures']):^{w_matchup}}"
            f"{str (row ['Full Time Score']):^{w_result}}"
            f"{str (row ['Venue']):^{w_venue}}"
        )
        print (row_str)