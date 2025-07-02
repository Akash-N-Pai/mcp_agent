# handlers.py

def list_jobs():
    return [
        {"id": "job1", "user": "akash", "status": "running"},
        {"id": "job2", "user": "bob", "status": "idle"}
    ]

def get_job(job_id):
    return {
        "id": job_id,
        "user": "akash",
        "status": "running",
        "cpus": 4,
        "memory": "4096 MB",
        "runtime": "2h30m"
    }

def cluster_status():
    return {
        "total_nodes": 20,
        "idle_nodes": 4,
        "cpu_utilization": "72%",
        "memory_usage": "128 GB / 256 GB"
    }
