# FIFA World Cup 2026 AI Tournament Simulator:

An end-to-end predictive modeling and tournament execution engine built in Python. The system ingests authentic 48-team tournament structures, processes full group stage tables, filters wildcards and executes a single-elimination knockout state machine driven by a trained **Random Forest Classifier** core.


## Predictive Analytics Matrix (Model Insights):

Rather than relying solely on historical bias, the engine evaluates real-time match variables using a trained Random Forest model. The relative feature importances from the latest championship simulation run break down as follows:

| Input Feature Dimension | Relative Importance Weight | Architectural Impact |
| :--- | :---: | :--- |
| **Form Rating** | `38.25%` | Primary driver; heavily rewards real-time team momentum streaks. |
| **Travel Fatigue** | `25.29%` | Dynamic stamina tax based on venue shifting and scheduling intervals. |
| **Squad Value** | `20.22%` | Financial/market value representation of squad player depth features. |
| **Rank Differential** | `16.25%` | Baseline historical performance weight tracking standard FIFA positions. |


## System Architecture & File Pipeline Details

The engine is built modularly across distinct functional domains to keep execution decoupled:

├── fixtures.csv               # Raw ingestion file containing 48-team schedule matrices
├── schedule_engine.py         # Main pipeline controller, table processor & wildcard evaluator
├── knockout_engine.py         # Elimination stage state machine with tie-breaker systems
├── ml_engine.py               # Model core inference wrangler and feature vector scalers
└── tournament_history.json    # Automated data persistence layer output (Saved tournament runs)


## Installation & Quickstart:

1. Clone the Workspace Directory:

git clone https://github.com/inanbiswas10/FIFA-World-Cup-2026-Simulation-Analytics-Engine.git
cd FIFA-World-Cup-2026-Simulation-Analytics-Engine

2. Install Pipeline Dependencies:

pip install pandas numpy scikit-learn

3. Execute the Simulation Loop:

python schedule_engine.py


## Sample Terminal Execution Log:

🚀 FIFA World Cup 2026 Best 3rd Place Teams Qualification Scenario (Round Of 32) 🚀
  Rank     Group              Team              Pts      GD      GF  
----------------------------------------------------------------------
   1         H              Uruguay              4       0       4   
   2         E              Ecuador              4      -1       3   
   3         J              Austria              3       0       3   

🚀 FIFA World Cup 2026 Round of 32 Prediction (32 Teams) 🚀
Spain                vs               Morocco    Winner: Spain                (3-1)
Argentina            vs               Algeria    Winner: Argentina            (2-0)
Germany              vs               Uruguay    Winner: Germany              (1-1 After Extra Time)
France               vs                  Iran    Winner: France               (2-2 After Extra Time) (5-3 After Penalty Shootout)

===========================================================================
🏆👑 FIFA World Cup 2026 (USA, Canada, Mexico) Champions: SPAIN 👑🏆
===========================================================================
💾 File Saved Successfully: 'tournament_history.json' created in workspace root.
