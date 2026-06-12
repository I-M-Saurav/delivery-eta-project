import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Delhivery Network Intelligence",
    page_icon="🚚",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    hub_df = pd.read_csv('data/hub_bottleneck_scores.csv')
    corridor_stats = pd.read_csv('data/corridor_stats.csv')
    return hub_df, corridor_stats

@st.cache_resource
def load_graph():
    return nx.read_gexf('data/logistics_graph.gexf')

hub_df, corridor_stats = load_data()
G = load_graph()
hub_score_dict = dict(zip(hub_df['hub'], hub_df['bottleneck_score']))

# Title
st.title("🚚 Delhivery Network Intelligence Dashboard")
st.markdown("**Graph-Based ETA Optimization & Bottleneck Detection**")
st.divider()

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Hubs", f"{G.number_of_nodes():,}")
col2.metric("Total Corridors", f"{G.number_of_edges():,}")
col3.metric("Avg Delay Factor", "2.21x")
col4.metric("Graph Model MAE Improvement", "14.44 mins")

st.divider()

# Two column layout
left, right = st.columns([1, 1])

with left:
    st.subheader("🔴 Top Bottleneck Hubs")
    top_n = st.slider("Show top N hubs", 5, 20, 10, key="hub_slider")
    display_df = hub_df.iloc[:top_n][['hub', 'bottleneck_score',
                                      'betweenness', 'avg_delay',
                                      'in_degree', 'out_degree']].round(3)
    display_df.columns = ['Hub', 'Score', 'Betweenness',
                           'Avg Delay', 'In Routes', 'Out Routes']
    display_df = display_df.reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, height=400)

with right:
    st.subheader("📊 Model Performance")
    fig, ax = plt.subplots(figsize=(6, 4))
    models = ['Baseline\n(No Graph)', 'Graph-Enhanced']
    maes = [52.50, 38.06]
    colors = ['#4472C4', '#C00000']
    bars = ax.bar(models, maes, color=colors, edgecolor='black', width=0.4)
    ax.set_ylabel('MAE (minutes)')
    ax.set_title('ETA Prediction: Baseline vs Graph-Enhanced')
    for bar, val in zip(bars, maes):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.5,
                f'{val:.2f}', ha='center', fontweight='bold')
    st.pyplot(fig)

st.divider()

# Network graph
st.subheader("🗺️ Logistics Network — Bottleneck Hubs Highlighted")

top_hubs = hub_df.head(20)['hub'].tolist()
subgraph_nodes = set(top_hubs)
for hub in top_hubs:
    if hub in G:
        subgraph_nodes.update(list(G.neighbors(hub))[:2])

H = G.subgraph(subgraph_nodes)
node_colors = [hub_score_dict.get(n, 0) for n in H.nodes()]
node_sizes = [300 + hub_score_dict.get(n, 0) * 3000 for n in H.nodes()]

fig2, ax2 = plt.subplots(figsize=(14, 8))
pos = nx.spring_layout(H, seed=42, k=2)
nodes = nx.draw_networkx_nodes(H, pos, node_color=node_colors,
                                node_size=node_sizes,
                                cmap=plt.cm.Reds, alpha=0.9, ax=ax2)
nx.draw_networkx_edges(H, pos, alpha=0.3, arrows=True,
                       arrowsize=10, edge_color='gray', ax=ax2)
nx.draw_networkx_labels(H, pos, font_size=7,
                        font_weight='bold', ax=ax2)
plt.colorbar(nodes, ax=ax2, label='Bottleneck Score')
ax2.set_title('Delhivery Logistics Network\nDarker/Larger = Higher Bottleneck Score')
ax2.axis('off')
st.pyplot(fig2)

st.divider()

# Corridor explorer
st.subheader("🔍 Corridor Delay Explorer")
col_a, col_b = st.columns(2)

with col_a:
    min_delay = st.slider("Minimum delay factor", 1.0, 20.0, 5.0, key="delay_slider")

with col_b:
    route_filter = st.selectbox("Sort by", ['median_delay', 'trip_count'])

filtered = corridor_stats[corridor_stats['median_delay'] >= min_delay]\
    .sort_values(route_filter, ascending=False).head(15).reset_index(drop=True)

st.dataframe(filtered[['source_center', 'destination_center',
                         'median_delay', 'trip_count',
                         'median_actual_time', 'median_osrm_time']].round(2),
             use_container_width=True)

st.divider()
st.caption("Summer Analytics 2026 | Graph-Based Network Intelligence | Delhivery Dataset")