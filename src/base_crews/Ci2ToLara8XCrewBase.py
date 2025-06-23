import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, llm
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from langchain_ollama import OllamaLLM
from local_log.log import logger
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
os.environ["LITELLM_DEBUG"] = "true"
os.environ["LITELLM_LOG_LEVEL"] = "DEBUG" 

@CrewBase
class Ci2ToLara8XCrewBase():
    """Ci2ToLara8X crew Base class"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @property
    def llms(self):
        return {
            "ollama_codellama": OllamaLLM(model="codellama:7b-instruct")
        }

    @agent
    def php_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['php_developer'], # type: ignore[index]
            verbose=True
        )
    @agent
    def formatting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['formatting_agent'], # type: ignore[index]
            verbose=True
        )
    @task
    def php_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['php_developer_task'], # type: ignore[index]
        )
    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task'], # type: ignore[index]
            output_file="formatted_code.php", # Specify the output file for the formatting task
        )
    @crew
    def crew(self) -> Crew:
        """Creates the CiToLaraCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
