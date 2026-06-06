# Optimizing Delivery ETAs with Graph-Based Network Intelligence

**Summer Analytics 2026 | CAIC IIT Gandhinagar**  
**Dataset:** Delhivery Logistics Network (141,725 trips)

---

## Project Overview

This project builds a graph-based intelligence system for Delhivery's logistics network.
The entire delivery network is modeled as a directed graph — facilities as nodes, 
corridors as edges — to produce smarter ETA predictions, surface bottleneck hubs, 
and generate actionable recommendations for network operations.

---

## Key Results

| Metric | Value |
|--------|-------|
| Network size | 1,641 hubs, 2,741 corridors |
| Corridors with >20% delay | 94.2% |
| Baseline MAE | 52.50 minutes |
| Graph-Enhanced MAE | 38.06 minutes |
| Accuracy improvement | +11.63% trips within 15% of actual |
| FTL vs Carting classifier | 100% accuracy |

---

## Project Structure

delivery-eta-project/
├── data/
│   ├── delivery_data.csv          # Raw dataset
│   ├── clean_data.csv             # Cleaned dataset
│   ├── corridor_stats.csv         # Per-corridor delay statistics
│   ├── logistics_graph.gexf       # Saved graph file
│   └── hub_bottleneck_scores.csv  # Hub ranking scores
├── notebooks/
│   ├── 01_eda.ipynb               # Exploratory Data Analysis
│   ├── 02_graph_construction.ipynb # Graph building
│   ├── 03_bottleneck_analysis.ipynb # Centrality & bottleneck ranking
│   ├── 04_eta_prediction.ipynb    # Baseline vs Graph-Enhanced model
│   └── 05_ftl_carting.ipynb       # FTL vs Carting framework
├── outputs/                       # All plots and visualizations
├── memo/
│   └── network_operations_strategy_memo.md  # Final business deliverable
└── README.md


---

## Notebooks Summary

| Notebook | What it does |
|----------|-------------|
| 01_eda | Loads data, explores delay patterns, hub distributions |
| 02_graph_construction | Builds directed graph, identifies delayed corridors |
| 03_bottleneck_analysis | Computes betweenness centrality, ranks bottleneck hubs |
| 04_eta_prediction | Trains baseline XGBoost vs graph-enhanced model |
| 05_ftl_carting | Builds route-type classifier, quantifies time-cost tradeoff |

---

## Setup

```bash
git clone <repo-url>
cd delivery-eta-project
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn networkx scikit-learn jupyter xgboost
```

---

## Top Findings

1. **IND000000ACB** is the #1 bottleneck — sits on 22.9% of all delivery paths
2. Carting trips are delayed **2.74x** on average vs FTL at **2.07x**
3. Graph-enhanced model reduces prediction error by **14.44 minutes** per trip
4. Corridor IND208012AAA → IND209304AAA has **35x delay** — immediate audit needed
5. 25,998 FTL trips under 50km — cost inefficiency with no delay benefit

---

## Strategy Memo

See `memo/network_operations_strategy_memo.md` for the full consulting deliverable
including hub-specific interventions, estimated impact, and 90-day action plan.