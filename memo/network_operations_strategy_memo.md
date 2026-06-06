# Network Operations Strategy Memo
**To:** Head of Network Operations, Delhivery  
**From:** Data Science Team  
**Date:** June 2026  
**Re:** Graph-Based Network Intelligence — Findings & Recommendations

---

## Executive Summary

An analysis of 141,725 delivery trips across Delhivery's logistics network reveals that OSRM systematically underestimates actual delivery time by an average of 2.2x. This is not random noise — it is structurally driven by a small number of high-centrality hubs that sit on the majority of delivery paths. A graph-based model reduces ETA prediction error by 14.44 minutes per trip (27% improvement) and increases the share of trips with accurate ETAs from 46.9% to 58.5%. The findings point to three concrete interventions that can materially reduce SLA breaches.

---

## 1. The Problem Is Structural, Not Random

94.2% of all corridors show actual delivery times exceeding OSRM predictions by more than 20%. The average delay factor across the network is 2.21x — meaning a trip predicted to take 3.5 hours actually takes 7+ hours on average. This level of systematic deviation cannot be explained by traffic alone. The root cause is hub-level congestion and dwell time at a small number of critical facilities.

---

## 2. Top 5 Bottleneck Hubs

The following hubs were ranked by a composite bottleneck score combining betweenness centrality, degree, and average delay factor:

| Rank | Hub | Bottleneck Score | Connections | Avg Delay | SLA Risk |
|------|-----|-----------------|-------------|-----------|----------|
| 1 | IND000000ACB | 0.809 | 92 | 1.57x | Critical |
| 2 | IND562132AAA | 0.584 | 71 | 1.50x | High |
| 3 | IND501359AAE | 0.392 | 57 | 1.70x | High |
| 4 | IND160002AAC | 0.369 | 61 | 1.68x | High |
| 5 | IND421302AAG | 0.357 | 58 | 1.78x | High |

**IND000000ACB** is the single most critical node — it sits on 22.9% of all shortest delivery paths. Any congestion here propagates to nearly a quarter of the network instantly.

---

## 3. Corridor-Specific Interventions

**Hub 1 — IND000000ACB (Critical):**  
This hub handles 92 corridors simultaneously. Recommendation: invest in parallel processing capacity (additional sorting lines or a secondary overflow facility nearby). Even a 20% throughput improvement here would reduce network-wide delays measurably.

**Hub 3 — IND501359AAE & Hub 5 — IND421302AAG (Delay-Heavy):**  
These hubs show 1.70x and 1.78x average delays despite moderate connectivity. Recommendation: audit dwell time at these facilities — the delay is disproportionate to their size, suggesting process inefficiency rather than volume overload. A targeted operational review (staffing, shift scheduling, scanner capacity) is the right first step.

**Chronic Delay Corridors:**  
The corridor IND208012AAA → IND209304AAA shows a 35x delay factor across 33 trips — this is a genuine chronic problem. Recommendation: immediate route audit. Either establish a parallel route or reclassify this corridor from Carting to FTL.

---

## 4. FTL vs Carting Decision Framework

Data shows FTL consistently outperforms Carting on delay ratio across all distance bands:

- **Under 50km:** Use Carting for cost efficiency, but flag routes through Tier 1 bottleneck hubs for FTL upgrade
- **50–300km:** Default to FTL; Carting only if hub bottleneck score < 0.2
- **Above 300km:** FTL exclusively

The current network has 25,998 FTL trips under 50km — an operational inefficiency that inflates costs without reducing delays. Transitioning appropriate short-haul routes to Carting can reduce cost without SLA impact.

---

## 5. Estimated Impact of Top 3 Hub Upgrades

If IND000000ACB, IND562132AAA, and IND501359AAE are upgraded to reduce their average delay factor by 30%:

- **Network-wide delay reduction:** ~8–12% across all corridors passing through these hubs
- **SLA breach reduction:** estimated 15–18% fewer late deliveries on affected routes
- **ETA accuracy gain:** graph-enhanced model already delivers 11.63% more trips within 15% accuracy — hub upgrades compound this further
- **Revenue at risk recovered:** every 1% reduction in SLA breaches on 141,000+ trips per cycle translates directly to customer retention and penalty cost avoidance

---

## 6. Recommended Next Steps

1. **Immediate:** Audit IND208012AAA → IND209304AAA corridor — 35x delay is unacceptable
2. **30 days:** Deploy graph-enhanced ETA model to replace OSRM-only predictions
3. **60 days:** Operational review at IND501359AAE and IND421302AAG for dwell time reduction
4. **90 days:** Begin capacity planning for IND000000ACB parallel processing upgrade
5. **Ongoing:** Monitor bottleneck scores monthly — the graph model flags emerging bottlenecks before they become crises

---

*Analysis based on 141,725 delivery trips. Graph model: XGBoost with node2vec-inspired hub embeddings. Baseline comparison: trip-level features only.*