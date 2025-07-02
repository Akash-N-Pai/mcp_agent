import htcondor

def main():
    coll = htcondor.Collector()
    schedd = coll.locate(htcondor.DaemonTypes.Schedd)
    schedd_obj = htcondor.Schedd(schedd)
    
    # Query all jobs owned by you
    jobs = schedd_obj.query('Owner == "akashvnp"', ['ClusterId', 'ProcId', 'JobStatus'])
    
    print(f"Found {len(jobs)} jobs for user akashvnp:")
    for job in jobs:
        print(f"Job {job['ClusterId']}.{job['ProcId']} Status: {job['JobStatus']}")

if __name__ == "__main__":
    main()
