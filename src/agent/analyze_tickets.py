import json
import os
import time
from typing import Dict, Any, List

def analyze_tickets():
    tickets_path = "context/sample-tickets.json"
    output_path = "specs/003-customer-success-ai/discovery-log.md"
    
    if not os.path.exists(tickets_path):
        print(f"Error: {tickets_path} not found")
        return

    with open(tickets_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    stats = {
        "email": {"count": 0, "total_len": 0},
        "whatsapp": {"count": 0, "total_len": 0},
        "web_form": {"count": 0, "total_len": 0}
    }
    categories = {}
    escalations = 0

    for t in tickets:
        ch = t["channel"]
        stats[ch]["count"] += 1
        stats[ch]["total_len"] += len(t["content"])
        
        cat = t["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        if t["expected_action"] == "escalate":
            escalations += 1

    # Generate Log
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Discovery Log — Phase 1 Incubation\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n\n")
        
        f.write("## Channel Patterns Discovered\n\n")
        for ch, data in stats.items():
            avg_len = data["total_len"] / data["count"] if data["count"] > 0 else 0
            f.write(f"### {ch.replace('_', ' ').title()} Channel\n")
            f.write(f"- Total messages: {data['count']}\n")
            f.write(f"- Average length: {avg_len:.1f} {'words' if ch != 'whatsapp' else 'chars'}\n\n")

        f.write("## Top Issues Found\n\n")
        f.write("| Rank | Category | Frequency |\n")
        f.write("|------|----------|-----------|\n")
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for i, (cat, count) in enumerate(sorted_cats[:10], 1):
            f.write(f"| {i} | {cat} | {count} |\n")

        f.write(f"\n## Escalation Summary\n")
        f.write(f"- Total tickets analyzed: {len(tickets)}\n")
        f.write(f"- Tickets requiring escalation: {escalations} ({ (escalations/len(tickets))*100 :.1f}%)\n")

    print(f"Analysis complete. Log saved to {output_path}")

if __name__ == "__main__":
    analyze_tickets()
