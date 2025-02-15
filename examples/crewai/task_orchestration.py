#!/usr/bin/env python3
"""
CrewAI Task Orchestration Example demonstrating role-based workflows and task dependencies.
This example shows how different agents collaborate on a research and documentation project.
"""

import os
from dotenv import find_dotenv, load_dotenv
from termcolor import cprint
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

# Load environment variables
dotenv_path = find_dotenv()
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv()

# Initialize tools
search_tool = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

def create_agents():
    """Create agents with specific roles and tools."""

    # Project Manager Agent
    project_manager = Agent(
        role='Project Manager',
        goal='Coordinate research project and ensure quality deliverables',
        backstory="""You are an experienced project manager with expertise in
        coordinating research projects and ensuring high-quality deliverables.""",
        verbose=True,
        allow_delegation=True
    )

    # Research Agent
    researcher = Agent(
        role='Research Specialist',
        goal='Gather and analyze information about the assigned topic',
        backstory="""You are an expert researcher with a strong analytical mindset
        and experience in gathering comprehensive information.""",
        verbose=True,
        tools=[search_tool, wikipedia]
    )

    # Writer Agent
    writer = Agent(
        role='Technical Writer',
        goal='Create clear and comprehensive documentation',
        backstory="""You are a skilled technical writer with expertise in creating
        clear, well-structured documentation and reports.""",
        verbose=True
    )

    # QA Agent
    qa_specialist = Agent(
        role='QA Specialist',
        goal='Ensure accuracy and quality of all deliverables',
        backstory="""You are a detail-oriented quality assurance specialist
        with a focus on maintaining high standards.""",
        verbose=True
    )

    return project_manager, researcher, writer, qa_specialist

def create_tasks(project_manager, researcher, writer, qa_specialist):
    """Create sequential tasks with dependencies."""

    # Task 1: Research Planning
    research_planning = Task(
        description="""Plan the research approach for understanding AI agent frameworks.
        1. Define research objectives
        2. Identify key areas to investigate
        3. Create research timeline
        4. Specify deliverables""",
        agent=project_manager
    )

    # Task 2: Information Gathering
    information_gathering = Task(
        description="""Gather comprehensive information about AI agent frameworks:
        1. Current market leaders
        2. Technical capabilities
        3. Use cases
        4. Implementation approaches""",
        agent=researcher
    )

    # Task 3: Analysis
    analysis = Task(
        description="""Analyze the gathered information:
        1. Compare different frameworks
        2. Identify strengths and weaknesses
        3. Evaluate implementation complexity
        4. Assess scalability""",
        agent=researcher
    )

    # Task 4: Documentation
    documentation = Task(
        description="""Create comprehensive documentation:
        1. Framework overview
        2. Technical specifications
        3. Implementation guidelines
        4. Best practices""",
        agent=writer
    )

    # Task 5: Quality Assurance
    quality_assurance = Task(
        description="""Review all deliverables:
        1. Verify accuracy of information
        2. Check completeness
        3. Validate technical details
        4. Ensure clarity""",
        agent=qa_specialist
    )

    return [
        research_planning,
        information_gathering,
        analysis,
        documentation,
        quality_assurance
    ]

def main():
    """
    Main function to demonstrate CrewAI task orchestration.
    """
    # Create agents
    print("\nCreating agents...")
    agents = create_agents()

    # Create tasks
    print("\nDefining tasks...")
    tasks = create_tasks(*agents)

    # Create crew
    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        verbose=2,
        process=Process.sequential
    )

    # Execute tasks
    print("\nExecuting research project...")
    result = crew.kickoff()

    # Save results
    print("\nSaving results...")
    with open('research_output.md', 'w') as f:
        f.write(result)

    print("\nProject completed! Check research_output.md for results.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
