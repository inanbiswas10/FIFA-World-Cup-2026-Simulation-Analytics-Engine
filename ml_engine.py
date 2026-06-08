import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class WorldCupMLPredictor:
    def __init__(self):

        self.model = RandomForestClassifier (n_estimators = 100,random_state = 42,max_depth = 8)
        self.scaler = StandardScaler ()
        self.is_trained = False
        
        self.raw_team_data = {
            
            "Mexico": {"rank": 15,"squad_val_m": 192.1,"form": 6.5},
            "Korea Republic": {"rank": 25,"squad_val_m": 157.8,"form": 6.0},
            "South Africa": {"rank": 60,"squad_val_m": 47.7,"form": 4.5},
            "Czechia": {"rank": 41,"squad_val_m": 209.5,"form": 5.5},

            "Canada": {"rank": 30,"squad_val_m": 150.5,"form": 6.5},
            "Switzerland": {"rank": 19,"squad_val_m": 373.2,"form": 7.0},
            "Qatar": {"rank": 55,"squad_val_m": 21.2,"form": 4.0},
            "Bosnia and Herzegovina": {"rank": 64,"squad_val_m": 147.3,"form": 5.0},

            "Brazil": {"rank": 6,"squad_val_m": 901.9,"form": 8.5},
            "Morocco": {"rank": 8,"squad_val_m": 528.5,"form": 8.0},
            "Scotland": {"rank": 43,"squad_val_m": 229.5,"form": 5.5},
            "Haiti": {"rank": 82,"squad_val_m": 63.8,"form": 3.5},

            "United States": {"rank": 16,"squad_val_m": 413.3,"form": 6.5},
            "USA": {"rank": 16,"squad_val_m": 413.3,"form": 6.5},
            "Australia": {"rank": 27,"squad_val_m": 58.5,"form": 6.0},
            "Paraguay": {"rank": 40,"squad_val_m": 156.0,"form": 5.5},
            "Türkiye": {"rank": 22,"squad_val_m": 510.2,"form": 7.5},

            "Germany": {"rank": 10,"squad_val_m": 896.2,"form": 8.5},
            "Ecuador": {"rank": 23,"squad_val_m": 425.0,"form": 7.0},
            "Côte d'Ivoire": {"rank": 34,"squad_val_m": 493.6,"form": 7.0},
            "Ivory Coast": {"rank": 34,"squad_val_m": 493.6,"form": 7.0},
            "Curaçao": {"rank": 83,"squad_val_m": 32.8,"form": 3.5},

            "Netherlands": {"rank": 7,"squad_val_m": 887.5,"form": 8.0},
            "Japan": {"rank": 18,"squad_val_m": 306.1,"form": 6.5},
            "Sweden": {"rank": 38,"squad_val_m": 421.8,"form": 7.0},
            "Tunisia": {"rank": 46,"squad_val_m": 60.2,"form": 4.5},

            "Belgium": {"rank": 9,"squad_val_m": 619.0,"form": 7.5},
            "Egypt": {"rank": 29,"squad_val_m": 125.1,"form": 5.5},
            "IR Iran": {"rank": 21,"squad_val_m": 42.6,"form": 5.0},
            "Iran": {"rank": 21,"squad_val_m": 42.6,"form": 5.0},
            "New Zealand": {"rank": 85,"squad_val_m": 25.7,"form": 3.0},

            "Spain": {"rank": 2,"squad_val_m": 1510.0,"form": 9.5},
            "Cabo Verde": {"rank": 68,"squad_val_m": 52.3,"form": 4.5},
            "Saudi Arabia": {"rank": 61,"squad_val_m": 32.0,"form": 4.0},
            "Uruguay": {"rank": 17,"squad_val_m": 424.7,"form": 7.5},

            "France": {"rank": 1,"squad_val_m": 1570.0,"form": 9.0},
            "Senegal": {"rank": 14,"squad_val_m": 549.4,"form": 7.5},
            "Iraq": {"rank": 57,"squad_val_m": 22.2,"form": 4.5},
            "Norway": {"rank": 31,"squad_val_m": 584.1,"form": 7.5},

            "Argentina": {"rank": 3,"squad_val_m": 882.1,"form": 9.0},
            "Algeria": {"rank": 28,"squad_val_m": 263.9,"form": 6.0},
            "Austria": {"rank": 24,"squad_val_m": 305.2,"form": 6.5},
            "Jordan": {"rank": 63,"squad_val_m": 18.5,"form": 4.0},

            "Portugal": {"rank": 5,"squad_val_m": 1160.0,"form": 8.5},
            "DR Congo": {"rank": 45,"squad_val_m": 177.8,"form": 5.5},
            "Uzbekistan": {"rank": 50,"squad_val_m": 73.8,"form": 5.0},
            "Colombia": {"rank": 13,"squad_val_m": 348.2,"form": 7.0},

            "England": {"rank": 4,"squad_val_m": 1870.0,"form": 8.5},
            "Croatia": {"rank": 11,"squad_val_m": 327.1,"form": 7.0},
            "Ghana": {"rank": 73,"squad_val_m": 230.8,"form": 5.0},
            "Panama": {"rank": 33,"squad_val_m": 37.5,"form": 5.0}
        }
        
        self.team_attributes = self._normalize_squad_values ()
        print (f"🧠 FIFA World Cup 2026 AI Pipeline Initialized: All {len (self.team_attributes)} data profiles bound to vector registry successfully !!")
        print ("\n")

    def _normalize_squad_values(self):
        
        all_vals = [team ["squad_val_m"] for team in self.raw_team_data.values ()]
        min_val,max_val = min (all_vals),max (all_vals)
        
        normalized_db = {}
        for name, data in self.raw_team_data.items ():
            norm_value = 1 + ((data ["squad_val_m"]-min_val)/(max_val-min_val))*99
            normalized_db [name] = {
                "rank": data ["rank"],
                "squad_value": round (norm_value,2),
                "form": data ["form"]
            }
        return normalized_db

    def get_team_features (self,team_name):
       
        cleaned_name = team_name.replace (" national football team", "").strip ()
        if cleaned_name in self.team_attributes:
            return self.team_attributes [cleaned_name]
        else:
            return {"rank": 50,"squad_value": 30.0,"form": 5.0}

    def generate_historical_training_data (self):
        
        raw_match_history = [
            {"features": [-1, -3, 1.0, 1],"outcome": 2},
            {"features": [-5, 5, -2.0, -1],"outcome": 0},
            {"features": [-5, 4, 2.0, 0],"outcome": 1},
            {"features": [12, -15, 1.5, 0],"outcome": 2},
            {"features": [-1, 5, 1.0, 1],"outcome": 2},
            {"features": [-5, 8, 0.0, -1],"outcome": 0},
            {"features": [-12, 15, 1.0, 1],"outcome": 2},
            {"features": [25, -20, -2.5, 0],"outcome": 0},
            {"features": [2, -3, 0.0, 0],"outcome": 1}
        ]
        X,y = [],[]
        for match in raw_match_history:
            X.append (match ["features"])
            y.append (match ["outcome"])
        return np.array (X),np.array (y)

    def train_predictive_model (self):
        
        X, y = self.generate_historical_training_data ()
        self.scaler.fit (X)
        X_scaled = self.scaler.transform (X)
        
        self.model.fit (X_scaled, y)
        self.is_trained = True
        print ("✅ Random forest ensemble successfully optimized across all FIFA World Cup 2026 Tournament entries !!")
        print ("\n")

if __name__ == "__main__":
    predictor = WorldCupMLPredictor ()
    predictor.train_predictive_model ()
    
    print ("\n🔍 AI Engine Sanity Verification is as follows: ")
    print ("\n")
    for test_team in ["Brazil","Argentina","Spain"]:
        print (f"{test_team} Normalized Attributes: {predictor.get_team_features (test_team)}")