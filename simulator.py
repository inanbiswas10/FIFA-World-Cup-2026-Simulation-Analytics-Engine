import numpy as np

class MatchSimulator:
    def __init__(self):
        pass

    def simulate_match (self,lambda_a,lambda_b):
        home_goals = int (np.random.poisson (lambda_a))
        away_goals = int (np.random.poisson (lambda_b))
        
        if home_goals > away_goals:
            points_a,points_b = 3,0
        elif home_goals < away_goals:
            points_a,points_b = 0,3
        else:
            points_a,points_b = 1,1
            
        return home_goals,away_goals,points_a,points_b