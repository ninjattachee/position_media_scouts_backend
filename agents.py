from crewai import Agent
from crewai_tools import SerperDevTool
from langchain_openai.chat_models.base import ChatOpenAI

from tools.youtube_search_tools import YoutubeVideoSearchTool

class CompanyResearchAgents:
    def __init__(self):
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.searchInternetTool = SerperDevTool()
        self.llm = ChatOpenAI(model="gpt-4.1")

    def research_manager(self, campanies: list[str], positions: list[str]) -> Agent:
        return Agent(
            role="Company Research Manager",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and the url and title for 3 recent YouTube interviews, for each position in each company.

            Companies: {campanies}
            Positions: {positions}

            Important:
            - The final list of JSON objects must include all companies and positions. Do not leave any out.
            - If you can't find information for a specific position, fill in the information with the word "MISSING".
            - Do not make up any information. Only return the information you find. Nothing else!
            - Do not stop researching until you find the requested information for each position in each company.
            - All the companies and positions exist so keep researching until you find the information for each one.
            - Make sure each researched position for each company contains 3 blog articles and 3 YouTube interviews.
            """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information into a list.""",
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
            allow_delegation=True,
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal=f"""Look up the specific positions for a given company and find urls for 3 recent blog articles and the url and title for 3 recent YouTube interviews for each person in the specified positions. It is your job to return this collected information in a JSON object.

            Important:
            - Once you've found the information, immediately stop searching for additional information.
            - Only return the requested information. Nothing else!
            - Make sure you find the persons name who holds the position.
            - Do not make up any information. Only return the information you find.
            """,
            backstory=f"""As a Company Research Agent, you are responsible for researching the company and the position and gathering relevant information.""",
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
        )
