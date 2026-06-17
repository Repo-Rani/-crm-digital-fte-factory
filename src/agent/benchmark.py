import json
import time
import os
from typing import List, Dict, Any
from src.agent.prototype_agent import CustomerSuccessAgent
from src.agent.models import Channel

def run_benchmark():
    agent = CustomerSuccessAgent()
    tickets_path = "context/sample-tickets.json"
    output_path = "specs/003-customer-success-ai/performance-baseline.md"
    
    if not os.path.exists(tickets_path):
        print(f"Error: {tickets_path} not found")
        return

    with open(tickets_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    results = []
    total_latency = 0
    correct_actions = 0
    correct_escalations = 0
    total_escalations_expected = 0
    
    print(f"Running benchmark on {len(tickets)} tickets...")

    for ticket in tickets:
        start_time = time.time()
        
        # Prepare raw message based on channel
        raw_msg = {
            "channel": ticket["channel"],
            "customer_name": ticket["customer_name"],
            "timestamp": ticket["timestamp"],
            "content": ticket["content"]
        }
        if ticket["channel"] == "email":
            raw_msg["customer_email"] = ticket["customer_email"]
            raw_msg["subject"] = ticket["subject"]
        elif ticket["channel"] == "whatsapp":
            raw_msg["customer_phone"] = ticket["customer_phone"]
        elif ticket["channel"] == "web_form":
            raw_msg["customer_email"] = ticket["customer_email"]
            raw_msg["message"] = ticket["content"]

        response = agent.process_message(raw_msg)
        latency = (time.time() - start_time) * 1000
        total_latency += latency
        
        # Validation
        is_escalation_correct = response.should_escalate == (ticket["expected_action"] == "escalate")
        if ticket["expected_action"] == "escalate":
            total_escalations_expected += 1
            if is_escalation_correct:
                correct_escalations += 1
        
        if is_escalation_correct:
            correct_actions += 1
            
        results.append({
            "id": ticket["id"],
            "channel": ticket["channel"],
            "expected": ticket["expected_action"],
            "actual": "escalate" if response.should_escalate else "answer",
            "latency_ms": int(latency),
            "pass": is_escalation_correct
        })

    avg_latency = total_latency / len(tickets)
    accuracy = (correct_actions / len(tickets)) * 100
    esc_accuracy = (correct_escalations / total_escalations_expected) * 100 if total_escalations_expected > 0 else 100

    # Generate Report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Performance Baseline — Phase 1 Prototype\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n")
        f.write(f"**Tickets tested:** {len(tickets)}\n\n")
        
        f.write("## Summary Metrics\n\n")
        f.write("| Metric | Achieved | Target | Pass? |\n")
        f.write("|--------|----------|--------|-------|\n")
        f.write(f"| Overall accuracy | {accuracy:.1f}% | >85% | {'✅' if accuracy >= 85 else '❌'} |\n")
        f.write(f"| Avg response time | {avg_latency:.0f}ms | <3000ms | {'✅' if avg_latency < 3000 else '❌'} |\n")
        f.write(f"| Correct escalation decisions | {esc_accuracy:.1f}% | >90% | {'✅' if esc_accuracy >= 90 else '❌'} |\n\n")
        
        f.write("## Detailed Results\n\n")
        f.write("| ID | Channel | Expected | Actual | Latency | Pass |\n")
        f.write("|----|---------|----------|--------|---------|------|\n")
        for r in results:
            f.write(f"| {r['id']} | {r['channel']} | {r['expected']} | {r['actual']} | {r['latency_ms']}ms | {'✅' if r['pass'] else '❌'} |\n")

    print(f"Benchmark complete. Report saved to {output_path}")

if __name__ == "__main__":
    run_benchmark()
