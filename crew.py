from agents import CompanyResearchAgents
from crewai import Crew
from job_manager import append_event
from task import CompanyResearchTasks


class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None

    def setup_crew(self, companies: list[str], positions: list[str]):
        print(f"Setting up crew for {companies} with positions {positions} and job_id {self.job_id}")

        # Setup agents
        agents = CompanyResearchAgents()
        research_manager = agents.research_manager(companies, positions)
        company_research_agent = agents.company_research_agent()

        # Setup tasks
        tasks = CompanyResearchTasks(self.job_id)
        company_research_tasks = [tasks.company_research(company_research_agent, company, positions) for company in companies]
        manage_research_task = tasks.manage_research(research_manager, companies, positions, company_research_tasks)

        # Setup crew
        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_tasks, manage_research_task],
            verbose=2
        )

    def kickoff(self):
        if self.crew is None:
            print(f"Crew is not setup for job {self.job_id}")
            append_event(self.job_id, "Crew is not setup")
            return "Crew is not setup"

        append_event(self.job_id, "Kicking off crew")

        try:
            print(f"Kicking off crew for job {self.job_id}")
            results = self.crew.kickoff()
            append_event(self.job_id, f"Crew completed")
            return results
        except Exception as e:
            print(f"Error kicking off crew for job {self.job_id}: {e}")
            append_event(self.job_id, f"Error kicking off crew: {e}")
            return str(e)
