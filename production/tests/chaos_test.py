import os
import time
import subprocess
import random
import json
from datetime import datetime

# Chaos Test: Pod Kills and Recovery
# US2 Requirement: Survival of pod kills every 2 hours

class ChaosMonkey:
    def __init__(self, namespace="customer-success-fte"):
        self.namespace = namespace
        self.results = []

    def get_pods(self, component):
        cmd = f"kubectl get pods -n {self.namespace} -l component={component} -o json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        return [p['metadata']['name'] for p in data['items']]

    def kill_pod(self, pod_name):
        print(f"[{datetime.now()}] 🐒 Chaos Monkey killing pod: {pod_name}")
        cmd = f"kubectl delete pod {pod_name} -n {self.namespace} --grace-period=0 --force"
        subprocess.run(cmd, shell=True)

    def run_chaos_cycle(self):
        components = ["api", "message-processor"]
        for comp in components:
            pods = self.get_pods(comp)
            if pods:
                target = random.choice(pods)
                self.kill_pod(target)
                self.results.append({"time": datetime.now().isoformat(), "pod": target, "component": comp, "action": "kill"})
        
        # Verify recovery (wait 30s)
        time.sleep(30)
        for comp in components:
            new_pods = self.get_pods(comp)
            print(f"[{datetime.now()}] Component {comp} has {len(new_pods)} pods active.")

    def save_report(self):
        with open("production/chaos_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    monkey = ChaosMonkey()
    print("Starting Chaos Test Cycle...")
    try:
        # For simulation, run 3 cycles
        for _ in range(3):
            monkey.run_chaos_cycle()
            print("Waiting 10 minutes for next chaos event...")
            time.sleep(600) 
    except KeyboardInterrupt:
        pass
    finally:
        monkey.save_report()
