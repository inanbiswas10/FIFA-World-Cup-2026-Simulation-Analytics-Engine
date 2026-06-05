import pandas as pd

class Tournament_Data_Pipeline:
    def __init__(self,fixtures_csv):
        try:
            self.fixtures_df = pd.read_csv (fixtures_csv)
            self.fixtures_df.columns = self.fixtures_df.columns.str.strip ()
            
            home_teams = self.fixtures_df ["home_team"].unique ()
            away_teams = self.fixtures_df ["away_team"].unique ()
            all_teams = list (set (home_teams) | set (away_teams))
            
            self.teams_df = pd.DataFrame (index = all_teams)
            self.teams_df ["base_lambda"] = 1.50
            
            print (f"📊 FIFA World Cup 2026 Pipeline Database Synced: {len (self.teams_df)} Teams Initialized from Fixtures Successfully !!")
            
        except FileNotFoundError:
            raise FileNotFoundError (f"❌ Error: The database file '{fixtures_csv}' was not found.")

    def calculate_match_lambdas (self,home_team,away_team):
        home_team = str (home_team).strip ()
        away_team = str (away_team).strip ()

        if home_team not in self.teams_df.index:
            raise ValueError (f"Team '{home_team}' is missing from the tournament index.")
        if away_team not in self.teams_df.index:
            raise ValueError (f"Team '{away_team}' is missing from the tournament index.")

        lambda_a = self.teams_df.loc [home_team,"base_lambda"]
        lambda_b = self.teams_df.loc [away_team,"base_lambda"]

        return lambda_a, lambda_b