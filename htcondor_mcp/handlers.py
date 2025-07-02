import htcondor


def interpret_status(code):
    """Convert numeric HTCondor job status to string."""
    return {
        1: "Idle",
        2: "Running",
        3: "Removed",
        4: "Completed",
        5: "Held",
        6: "Transferring Output",
        7: "Suspended"
    }.get(code, f"Unknown ({code})")


def list_jobs():
    """Return a list of current jobs from the HTCondor scheduler."""
    schedd = htcondor.Schedd()
    jobs = schedd.query(
        constraint="true",  # get all jobs
        projection=[
            'ClusterId', 'JobStatus', 'Owner',
            'Cmd', 'RequestCpus', 'RequestMemory'
        ]
    )

    job_list = []
    for job in jobs:
        job_dict = {
            "id": str(job.get("ClusterId")),
            "owner": job.get("Owner"),
            "status": interpret_status(job.get("JobStatus")),
            "cmd": job.get("Cmd", "N/A"),
            "cpus": job.get("RequestCpus", "N/A"),
            "memory": job.get("RequestMemory", "N/A")
        }
        job_list.append(job_dict)

    return job_list


def get_job(job_id):
    """Return detailed info for a single job by ClusterId."""
    schedd = htcondor.Schedd()
    jobs = schedd.query(
        constraint=f"ClusterId == {job_id}",
        projection=[
            'Owner', 'JobStatus', 'Cmd',
            'RequestCpus', 'RequestMemory', 'EnteredCurrentStatus'
        ]
    )

    if not jobs:
        return {"error": f"No job found with ID {job_id}"}

    job = jobs[0]
    return {
        "id": str(job_id),
        "owner": job.get("Owner"),
        "status": interpret_status(job.get("JobStatus")),
        "cmd": job.get("Cmd", "N/A"),
        "cpus": job.get("RequestCpus", "N/A"),
        "memory": job.get("RequestMemory", "N/A"),
        "entered_status_at": job.get("EnteredCurrentStatus")
    }


def cluster_status():
    """Summarize cluster node usage from the HTCondor collector."""
    coll = htcondor.Collector()
    ads = coll.query(
        htcondor.AdTypes.Startd,
        projection=['Name', 'State', 'Cpus', 'Memory']
    )

    total_nodes = len(ads)
    idle_nodes = sum(1 for ad in ads if ad.get("State") == "Unclaimed")
    busy_nodes = sum(1 for ad in ads if ad.get("State") == "Claimed")

    return {
        "total_nodes": total_nodes,
        "idle_nodes": idle_nodes,
        "busy_nodes": busy_nodes
    }
