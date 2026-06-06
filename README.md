# ⚽ FIFA World Cup 2026 Predictive Simulation Engine 🏆

A data-driven, stateful simulation engine built in Python to forecast match outcomes and tournament progression for the expanded 48-team FIFA World Cup 2026. This project leverages historical international football metrics, probabilistic sports analytics, and dynamic state management to build public software architecture.

---

## 🛠️ Project Architecture & Daily Progression

### 🗓️ Day 1: Data Ingestion & Preprocessing Pipeline
* **Robust Feature Ingestion:** Built a custom data pipeline using `pandas` to load, sanitize, and validate the official World Cup 2026 match schedule.
* **Vectorized Data Handling:** Formatted critical match attributes including group boundaries, historical match metrics, venue vectors, and timezone-adjusted kickoff times (IST).
* **Defensive Error Isolation:** Integrated structured exception-handling blocks (`try-except`) across the processing loop to isolate data structural formatting discrepancies without halting pipeline streaming.

---

### 🗓️ Day 2: Probabilistic Match Simulation Core
* **Poisson Distribution Integration:** Developed a core match simulator (`MatchSimulator`) using probabilistic models to evaluate offensive and defensive team strengths.
* **Dynamic Score Matrix Generator:** Designed a scoring engine that models international football matches as random, independent statistical variables based on real-time team lambda scoring rates.
* **Decoupled System Modules:** Maintained a clean, production-grade separation of concerns by isolating data ingestion mechanics (`pipeline.py`) completely from the mathematical simulation layers (`simulator.py`).

---

### 🗓️ Day 3: Stateful Tournament Engine & Advancement Vector Extraction

#### System Architecture Evolution
The `World_Cup_Schedule_Engine` has been refactored from a flat data parser into a stateful **Tournament Prediction Machine**. The architecture smoothly decouples data ingestion, in-memory state mutation, and conditional UI rendering.

#### Key Architectural Implementations:
* **In-Memory State Tracking:** Engineered a multidimensional dictionary matrix (`self.standings`) to persist real-time tournament metrics—Games Played ($P$), Wins ($W$), Draws ($D$), Losses ($L$), Goals For ($GF$), Goals Against ($GA$), Goal Difference ($GD$), and Points ($Pts$)—across all 48 participating countries simultaneously.
* **Defensive Memory Allocation:** Implemented a private initialization helper (`_initialize_team_standing`) to allocate team data structures dynamically during execution and prevent runtime initialization errors.
* **Algorithmic Sorting Engine:** Integrated strict FIFA tie-breaker hierarchies. The system uses composite, multi-key Python `lambda` functions to sort group standings sequentially on the fly:
  
  $$\text{Total Points (Pts)} \rightarrow \text{Goal Difference (GD)} \rightarrow \text{Goals For (GF)}$$

* **Advancement Vector Extraction:** Developed a decoupled extraction layer (`extract_group_qualifiers`) that programmatically slices indices `[0]` and `[1]` from each sorted group matrix to harvest the top 24 automatic qualifiers for the Round of 32.
* **Scannable Terminal Dashboard:** Upgraded the UI presentation layer with context-switching variable monitors. The script dynamically injects vertical spacing boundaries upon detecting group transitions, delivering a highly readable console output.

---

## 💻 Tech Stack
* **Language:** Python 3.x
* **Data Libraries:** Pandas
* **Mathematical Core:** SciPy / NumPy (Probabilistic Math)
* **Version Control:** Git & GitHub Desktop

---

## 🚀 How to Run the Project
Ensure you have your environment dependencies installed, then execute the schedule engine script:

```bash
pip install pandas scipy
python schedule_engine.py
