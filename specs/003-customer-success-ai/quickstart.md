# Quickstart: Customer Success AI Agent (Phase 1 Prototype)

Follow these instructions to set up and run the Phase 1 incubation prototype.

## 1. Prerequisites
- Python 3.10 or higher
- `pip` (Python package installer)

## 2. Installation
1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For Phase 1, the primary dependency is the `mcp` SDK.*

3. Set up environment (optional but recommended):
   ```bash
   # Linux/macOS
   export PYTHONPATH=$PYTHONPATH:.
   # Windows (PowerShell)
   $env:PYTHONPATH="."
   ```

## 3. Running the Core Agent
You can test the agent logic directly using the prototype script:
```bash
# Ensure PYTHONPATH is set
python src/agent/prototype_agent.py
```
This will run the built-in test cases and display normalized messages, sentiment scores, and generated responses.

## 4. Starting the MCP Server
To expose the agent tools via MCP:
```bash
python mcp_server/server.py
```
The server will start on `stdio` and can be connected to any MCP-compatible client (like Claude Desktop).

## 5. Running the Benchmarks
To evaluate the agent's performance across all 60 sample tickets:
```bash
python src/agent/benchmark.py
```
This script will output accuracy metrics, average latency, and channel compliance reports to `specs/003-customer-success-ai/performance-baseline.md`.

## 6. Running Tests
Execute the comprehensive test suite using `pytest`:
```bash
pytest tests/ -v
```
*Note: pytest handles the path mapping automatically.*

