import random
from locust import HttpUser, task, between, events

class WebFormUser(HttpUser):
    """Simulates high-volume web form traffic."""
    wait_time = between(2, 10)
    weight = 3  # Most common channel

    @task
    def submit_support_form(self):
        categories = ['general', 'technical', 'billing', 'feedback', 'bug_report']
        priorities = ['low', 'medium', 'high']
        
        self.client.post("/support/submit", json={
            "name": f"Load Test User {random.randint(1, 10000)}",
            "email": f"loadtest_{random.randint(1, 10000)}@example.com",
            "subject": f"Load Test Query {random.randint(1, 100)}",
            "category": random.choice(categories),
            "priority": random.choice(priorities),
            "message": "This is a load test message to verify system performance under stress. We are checking if the Kafka producer and the database can handle concurrent submissions without dropping data."
        })

class HealthCheckUser(HttpUser):
    """Simulates background monitoring traffic."""
    wait_time = between(5, 15)
    weight = 1

    @task(2)
    def check_health(self):
        self.client.get("/health")

    @task(1)
    def check_metrics(self):
        self.client.get("/metrics/channels")

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--test-id", type=str, env_var="TEST_ID", default="load-test-001")
