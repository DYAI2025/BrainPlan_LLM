import networkx as nx
import json
from typing import List, Dict, Any
from .scoring import Thought, calculate_total_score
from .llm import llm

RELATIONS = ["ergänzt", "widerspricht", "abhängig_von", "kombinierbar", "besser_als"]

def classify_relation(t1: Thought, t2: Thought) -> str:
    """
    Classify the relationship between two thoughts.
    In a real implementation, this would use LLM to analyze the relationship.
    For now, we'll use simple heuristics based on scores and content.
    """
    # In a production implementation, we would use an LLM to analyze the relationship
    if abs(t1.total_score - t2.total_score) > 2.0:
        return "besser_als" if t1.total_score > t2.total_score else "besser_als"
    if "API" in t1.summary and "Bot" in t2.summary:
        return "kombinierbar"
    if "Server" in t1.summary and "PWA" in t2.summary:
        return "widerspricht"
    return "ergänzt"

def rate_strength(relation: str) -> int:
    """
    Rate the strength of a relationship from 1-5.
    """
    strength_map = {
        "kombinierbar": 5,
        "ergänzt": 4,
        "besser_als": 3,
        "abhängig_von": 2,
        "widerspricht": 1
    }
    return strength_map.get(relation, 3)

def run_graph_of_thoughts(thoughts: List[Thought]) -> dict:
    """
    Execute the Graph-of-Thoughts algorithm on a set of thoughts.
    """
    G = nx.DiGraph()

    # Add nodes (thoughts) to the graph
    for t in thoughts:
        G.add_node(t.id, thought=t, score=t.total_score)

    # Create edges between thoughts based on relationships
    for i in range(len(thoughts)):
        for j in range(i + 1, len(thoughts)):
            rel = classify_relation(thoughts[i], thoughts[j])
            weight = rate_strength(rel)
            G.add_edge(thoughts[i].id, thoughts[j].id, relation=rel, weight=weight)
            G.add_edge(thoughts[j].id, thoughts[i].id, relation="inverse_" + rel, weight=weight)

    # Detect clusters using Louvain algorithm
    try:
        import community as community_louvain
        partition = community_louvain.best_partition(G.to_undirected())
    except ImportError:
        # If python-louvain is not available, assign all nodes to the same cluster
        partition = {n: 0 for n in G.nodes}

    # Calculate betweenness centrality to find bridge thoughts
    betweenness = nx.betweenness_centrality(G)

    # Generate hybrid thoughts from clusters
    hybrids = []
    for cluster_id in set(partition.values()):
        nodes = [n for n, c in partition.items() if c == cluster_id]
        if len(nodes) >= 2:  # Changed from 3 to 2 to ensure we get some clusters
            # Get the thoughts in this cluster
            cluster_thoughts = [G.nodes[n]['thought'] for n in nodes if n in G.nodes]
            if cluster_thoughts:
                # Calculate average score for the cluster
                avg_score = sum([t.total_score for t in cluster_thoughts]) / len(cluster_thoughts)
                # Apply cluster bonus (15% boost for being in a strong cluster)
                hybrid_score = min(avg_score * 1.15, 10.0)
                
                # Create a summary for the hybrid thought
                cluster_summaries = [G.nodes[n]['thought'].summary for n in nodes if n in G.nodes]
                hybrid_summary = f"Hybrid aus den Gedanken: {', '.join(nodes)}\n\nKombiniert die Ansätze:\n" + "\n\n".join(cluster_summaries[:2])  # Limit to first 2 for brevity
                
                hybrids.append({
                    "id": f"HYBRID_C{cluster_id}",
                    "components": nodes,
                    "score": hybrid_score,
                    "summary": hybrid_summary
                })

    # Find the best hybrid based on score and centrality
    if hybrids:
        best = max(hybrids, key=lambda h: h["score"])
    else:
        # If no hybrids were created, return None
        best = None

    # Create visualization of the graph (simplified representation)
    visualization = {
        "nodes": [{"id": n, "score": G.nodes[n]["score"], "summary": G.nodes[n]["thought"].summary[:50] + "..."} for n in G.nodes],
        "edges": [{"source": u, "target": v, "relation": d["relation"], "weight": d["weight"]} for u, v, d in G.edges(data=True)],
        "clusters": partition,
        "best_hybrid": best
    }

    return {
        "graph": G,
        "visualization": visualization,
        "hybrids": hybrids,
        "best_hybrid": best,
        "clusters": len(set(partition.values())),
        "bridge_thoughts": sorted(betweenness, key=betweenness.get, reverse=True)[:3]
    }

def run_full_tot_then_got(task: str, use_mock: bool = False) -> dict:
    """
    Run the complete pipeline: Tree-of-Thoughts followed by Graph-of-Thoughts.
    """
    from .tree_of_thoughts import tree_of_thoughts_live

    # 1. Run Tree-of-Thoughts to generate initial thoughts
    if use_mock:
        print("Phase 2a: Tree-of-Thoughts mit Mock-Daten...")
    else:
        print("Phase 2a: Tree-of-Thoughts mit echtem LLM...")

    tot_thoughts = tree_of_thoughts_live(task, use_mock=use_mock)
    print(f"ToT fertig – {len(tot_thoughts)} beste Thoughts generiert")

    # 2. Run Graph-of-Thoughts on the ToT results
    print("Phase 2b: Graph-of-Thoughts – analysiert Beziehungen...")
    got_result = run_graph_of_thoughts(tot_thoughts)
    print(f"GoT fertig – {got_result['clusters']} Cluster gefunden")

    return {
        "tot_thoughts": tot_thoughts,
        "got_result": got_result,
        "final_hybrid": got_result["best_hybrid"]
    }