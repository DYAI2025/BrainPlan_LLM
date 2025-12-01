def render_mermaid(G, highlight_id=None, visualization_data=None):
    """
    Render a Mermaid diagram for the graph of thoughts.
    If visualization_data is provided, use that instead of the NetworkX graph.
    """
    if visualization_data:
        # Use the visualization data structure instead of NetworkX graph
        lines = ['graph TD']
        
        # Add nodes
        for node in visualization_data["nodes"]:
            label = node["id"].replace("Thought", "T").replace("HYBRID", "H")
            score = f"{node['score']:.2f}"
            line = f'    {node["id"]}[{label}<br>Score {score}]'
            if node["id"] == highlight_id:
                line += ':::highlight'
            lines.append(line)

        # Add edges
        for edge in visualization_data["edges"]:
            rel = edge['relation'].replace("inverse_", "")
            lines.append(f'    {edge["source"]} -->|{rel} {edge["weight"]}| {edge["target"]}')

        lines.append("    classDef highlight fill:#116,stroke:#0f0,stroke-width:4px")
        return "```mermaid\n" + "\n".join(lines) + "\n```"
    else:
        # Original implementation using NetworkX graph
        lines = ['graph TD']
        for node in G.nodes:
            label = node.replace("Thought", "T").replace("HYBRID", "H")
            score = f"{G.nodes[node].get('score', 0):.2f}"
            line = f'    {node}[{label}<br>Score {score}]'
            if node == highlight_id:
                line += ':::highlight'
            lines.append(line)

        for u, v, data in G.edges(data=True):
            rel = data['relation'].replace("inverse_", "")
            lines.append(f'    {u} -->|{rel} {data["weight"]}| {v}')

        lines.append("    classDef highlight fill:#116,stroke:#0f0,stroke-width:4px")
        return "```mermaid\n" + "\n".join(lines) + "\n```"

def generate_thought_summary(thoughts):
    """
    Generate a text summary of thoughts.
    """
    summary = "## Gedanken-Übersicht\n\n"
    for thought in thoughts:
        summary += f"### {thought.id} (Score: {thought.total_score:.2f})\n"
        summary += f"{thought.summary}\n\n"
        summary += "Bewertung nach Kriterien:\n"
        for criterion, score in thought.criteria_scores.items():
            summary += f"- {criterion}: {score}/10\n"
        summary += "\n"
    return summary

def generate_hybrid_summary(hybrids):
    """
    Generate a text summary of hybrid thoughts.
    """
    if not hybrids:
        return "## Hybride Gedanken\n\nKeine Hybride generiert.\n"
    
    summary = "## Hybride Gedanken\n\n"
    for hybrid in hybrids:
        summary += f"### {hybrid['id']} (Score: {hybrid['score']:.2f})\n"
        summary += f"Komponenten: {', '.join(hybrid['components'])}\n"
        summary += f"Zusammenfassung: {hybrid['summary']}\n\n"
    return summary