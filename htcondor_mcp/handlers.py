# handlers.py

import htcondor

def list_jobs():
    schedd = htcondor.Schedd()
    # Only fetch running/idle/held jobs (not completed)
    jobs = schedd.query(
        constraint='true',
        projection=['ClusterId', 'JobStatus', 'Owner', 'Cmd', 'RequestCpus', 'RequestMemory']
    )
    
    job_list = []
    for job in jobs:
        job_list.append({
            "id": f"{job['ClusterId']}",
            "owner": job['Owner'],
            "status": interpret_status(job['JobStatus']),
            "cmd": job.get('Cmd', 'N/A'),
            "cpus": job.get('RequestCpus', 'N/A'),
            "memory": job.get('RequestMemory', 'N/A')
        })

    return job_list

def get_job(job_id):
    schedd = htcondor.Schedd()
    jobs = schedd.query(
        constraint=f"ClusterId == {job_id}",
        projection=['Owner', 'JobStatus', 'Cmd', 'RequestCpus', 'RequestMemory', 'EnteredCurrentStatus']
    )
    if not jobs:
        return {"error": f"No job found with ID {job_id}"}
    
    job = jobs[0]
    return {
        "id": job_id,
        "owner": job['Owner'],
        "status": interpret_status(job['JobStatus']),
        "cmd": job.get('Cmd', 'N/A'),
        "cpus": job.get('RequestCpus', 'N/A'),
        "memory": job.get('RequestMemory', 'N/A'),
        "entered_status_at": job.get('EnteredCurrentStatus')
    }

def cluster_status():
    coll = htcondor.Collector()
    ad_list = coll.query(htcondor.AdTypes.Startd,
                         projection=['Name', 'State', 'Cpus', 'Memory'])

    total_nodes = len(ad_list)
    idle_nodes = sum(1 for ad in ad_list if ad.get("State") == "Unclaimed")
    busy_nodes = sum(1 for ad in ad_list if ad.get("State") == "Claimed")

    return {
        "total_nodes": total_nodes,
        "idle_nodes": idle_nodes,
        "busy_nodes": busy_nodes
    }

def interpret_status(code):
    return {
        1: "Idle",
        2: "Running",
        3: "Removed",
        4: "Completed",
        5: "Held",
        6: "Transferring Output",
        7: "Suspended"
    }.get(code, f"Unknown ({code})")
