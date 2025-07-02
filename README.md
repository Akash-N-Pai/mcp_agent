# HTCondor MCP Agent

## Overview

This project provides an agent-based system for monitoring and interacting with HTCondor jobs, particularly on the AF cluster at UChicago. It includes components for scraping job information, querying job status, and example scripts for submitting and managing jobs with HTCondor.

## Project Structure

- `agent_main/` — Main entry point for running the agent.
- `components/condor_job_scraper.py` — Scrapes job information from HTCondor and logs it as observations.
- `mcp_simple/mcp_agent.py` — Simple script to query and print jobs for a specific user.
- `practice_code_run/` — Example HTCondor job scripts and submission files.
- `config.yaml` — Configuration for the agent and its components.
- `htcondor_mcp/` — (Placeholder for server/handlers, currently empty)

## Requirements

- Python 3.8+
- [htcondor Python bindings](https://htcondor.readthedocs.io/en/latest/apis/python-bindings/index.html)
- (Optional) `google.adk` package for advanced agent/component features

Install dependencies (if requirements.txt is populated):
```bash
pip install -r mcp_simple/requirements.txt
pip install -r htcondor_mcp/requirements.txt
```
Or manually install:
```bash
pip install htcondor
```

## Configuration

The agent is configured via `config.yaml`:
```yaml
agent:
  id: condor_agent
  name: Condor HTCondor Agent
  description: Monitors HTCondor jobs on the AF.
  components:
    - id: condor_job_scraper
      path: components/condor_job_scraper.py
```

## Usage

### 1. Running the Agent

The main agent can be started with:
```bash
python -m agent_main
```
This will launch the agent, which uses the `CondorJobScraper` component to monitor jobs on the cluster.

### 2. Querying Jobs (Simple Script)

You can use the simple script in `mcp_simple/mcp_agent.py` to query jobs for a specific user:
```bash
python mcp_simple/mcp_agent.py
```
This will print all jobs owned by the user `akashvnp` (edit the script to change the username).

### 3. Submitting Example Jobs

In `practice_code_run/`, you will find example scripts for submitting jobs to HTCondor:
- `myjob.sh`: Example job script
- `myjob.sub`: HTCondor submission file

Submit a job with:
```bash
cd practice_code_run
condor_submit myjob.sub
```

### 4. Output and Logs

Job output, error, and log files will be generated in the `practice_code_run/` directory (e.g., `myjob.log`, `myjob.6092022.0.out`, `myjob.6092022.0.err`).

## Example: CondorJobScraper Component

The `CondorJobScraper` component queries all jobs and logs their status as observations:
```python
class CondorJobScraper(BaseComponent):
    def observe(self) -> list[Observation]:
        jobs = self.schedd.query()
        # ... process jobs ...
        return [Observation.create(...)]
```

## Notes
- The `htcondor_mcp/` directory is a placeholder for server/handler code and may be expanded in the future.
- The project references `google.adk` for agent/component abstractions. Ensure this package is available in your environment if using advanced features.

