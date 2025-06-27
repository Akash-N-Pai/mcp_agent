from google.adk.components import BaseComponent
from google.adk.schema import Observation
import htcondor
import datetime

class CondorJobScraper(BaseComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schedd = htcondor.Schedd()

    def observe(self) -> list[Observation]:
        jobs_info = []
        try:
            # Query jobs from condor_q
            jobs = self.schedd.query()

            for job in jobs:
                info = {
                    "JobId": f"{job['ClusterId']}.{job['ProcId']}",
                    "Owner": job.get("Owner", "unknown"),
                    "JobStatus": job.get("JobStatus", "unknown"),
                    "EnteredCurrentStatus": str(job.get("EnteredCurrentStatus", "unknown")),
                    "Cmd": job.get("Cmd", "unknown"),
                }
                jobs_info.append(info)

        except Exception as e:
            self.logger.error(f"Error scraping condor jobs: {e}")

        return [
            Observation.create(
                who="condor_job_scraper",
                what={"jobs": jobs_info},
                when=datetime.datetime.utcnow(),
                where="login01.af.uchicago.edu"
            )
        ]
