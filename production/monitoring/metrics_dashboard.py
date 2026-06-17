"""
Metrics Dashboard — Production
Simple CLI-based dashboard to monitor Digital FTE performance.
"""

import requests
import time
import os
import json
from datetime import datetime

API_URL = os.getenv('API_URL', 'http://localhost:8000')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_metrics():
    try:
        response = requests.get(f"{API_URL}/metrics/channels", timeout=5)
        return response.json()
    except Exception as e:
        return None

def fetch_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.json()
    except Exception as e:
        return None

def print_dashboard(metrics, health):
    clear_screen()
    print("=" * 60)
    print(f" DIGITAL FTE PERFORMANCE DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Health Section
    if health:
        status = health.get('status', 'unknown').upper()
        color = "\033[92m" if status == 'HEALTHY' else "\033[91m"
        print(f" SYSTEM STATUS: {color}{status}\033[0m")
        print(f" Version: {health.get('version', 'N/A')}")
        print("-" * 60)
    
    # Metrics Section
    if metrics:
        print(f" {'CHANNEL':<15} | {'TOTAL':<8} | {'RESOLVED':<10} | {'ESCALATED':<10}")
        print("-" * 60)
        
        total_all = 0
        esc_all = 0
        
        for channel, data in metrics.items():
            total = data.get('total', 0)
            res = data.get('resolved', 0)
            esc = data.get('escalated', 0)
            
            total_all += total
            esc_all += esc
            
            print(f" {channel.upper():<15} | {total:<8} | {res:<10} | {esc:<10}")
        
        print("-" * 60)
        esc_rate = (esc_all / total_all * 100) if total_all > 0 else 0
        print(f" TOTAL CONVERSATIONS: {total_all}")
        print(f" OVERALL ESCALATION RATE: {esc_rate:.2f}%")
        
        # Ground Truth check
        if esc_rate > 25:
            print("\033[91m [!] WARNING: Escalation rate exceeds 25% SLA threshold!\033[0m")
    else:
        print(" [!] ERROR: Could not fetch metrics from API.")
    
    print("=" * 60)
    print(" Press Ctrl+C to exit. Refreshing every 10s...")

def main():
    while True:
        metrics = fetch_metrics()
        health = fetch_health()
        print_dashboard(metrics, health)
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDashboard exited.")
