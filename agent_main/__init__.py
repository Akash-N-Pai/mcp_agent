from adk.agent import Agent
from adk.components import ComponentConfig
from components.condor_job_scraper import CondorJobScraper

def main():
    components = [
        CondorJobScraper(config=ComponentConfig(id="condor_job_scraper"))
    ]
    agent = Agent(
        id="condor_agent",
        name="Condor HTCondor Agent",
        description="Monitors HTCondor jobs on the AF.",
        components=components
    )
    agent.run()

if __name__ == "__main__":
    main()
