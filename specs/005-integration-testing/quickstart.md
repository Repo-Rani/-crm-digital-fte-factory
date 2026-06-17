# Quickstart: Phase 3 Integration & Testing

## 1. Prerequisites
- Docker & Docker Compose running.
- `kubectl` configured (if testing Kubernetes deployment).
- Python 3.11 environment with `pip install -r requirements.txt`.

## 2. Setting Up Test Environment
1. Create test env file:
   ```bash
   cp production/tests/.env.example production/tests/.env.test
   ```
2. Set `TEST_BASE_URL=http://localhost:8000`.

## 3. Running Validation Suite

### E2E Suite
```bash
pytest production/tests/test_multichannel_e2e.py -v
```

### Load Test
```bash
locust -f production/tests/load_test.py --host=http://localhost:8000 --users=50 --spawn-rate=5 --run-time=5m --headless
```

### Chaos Test
```bash
python production/tests/chaos_test.py --cycles=3
```

## 4. Starting the 24-Hour Simulation
Open a dedicated terminal and run:
```bash
python production/tests/test_24hr_simulation.py --duration=86400 --rate=8
```

## 5. Monitoring Real-Time Metrics
```bash
python production/monitoring/metrics_dashboard.py
```
This dashboard refreshes every 60 seconds and shows SLA compliance.
