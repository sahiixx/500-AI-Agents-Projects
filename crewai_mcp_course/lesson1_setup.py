"""
Lesson 1: Setting up CrewAI with MCP Server Access

This lesson covers:
- Installing required packages
- Setting up environment variables
- Creating a basic CrewAI agent
- Executing simple tasks

Learning Objectives:
- Understand CrewAI agent structure
- Configure environment for MCP server access
- Create and run a simple agent task
- Handle basic error scenarios
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def setup_environment():
    """
    Step 1: Set up environment variables
    
    Required environment variables:
    - OPENAI_API_KEY: Your OpenAI API key
    - FASTMCP_URL: FastMCP server URL (optional for this lesson)
    - FASTMCP_API_KEY: FastMCP API key (optional for this lesson)
    """
    print("=" * 60)
    print("LESSON 1: Setting up CrewAI with MCP Server Access")
    print("=" * 60)
    print()
    
    # Check for required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or export it:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print()
    else:
        print("✅ OPENAI_API_KEY found")
    
    # Optional MCP server configuration
    fastmcp_url = os.getenv("FASTMCP_URL", "http://localhost:8000")
    fastmcp_key = os.getenv("FASTMCP_API_KEY", "")
    
    print(f"📡 FastMCP Server URL: {fastmcp_url}")
    print(f"🔑 FastMCP API Key: {'Set' if fastmcp_key else 'Not set (optional for this lesson)'}")
    print()
    
    return {
        "openai_key": openai_key,
        "fastmcp_url": fastmcp_url,
        "fastmcp_key": fastmcp_key
    }


def create_basic_agent():
    """
    Step 2: Create a basic CrewAI agent
    
    An agent has:
    - role: The agent's job title/role
    - goal: What the agent aims to achieve
    - backstory: Context about the agent's expertise
    - verbose: Whether to print detailed logs
    - allow_delegation: Whether the agent can delegate tasks
    """
    print("=" * 60)
    print("Creating a Basic Research Agent")
    print("=" * 60)
    print()
    
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )
    
    # Create a research agent
    researcher = Agent(
        role="Research Analyst",
        goal="Gather and analyze information on given topics",
        backstory="""You are an experienced research analyst with a keen eye for detail.
        You excel at finding relevant information and presenting it in a clear,
        concise manner. Your analyses are always thorough and well-structured.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    print("✅ Research Agent created successfully!")
    print(f"   Role: {researcher.role}")
    print(f"   Goal: {researcher.goal}")
    print()
    
    return researcher


def create_simple_task(agent):
    """
    Step 3: Create a simple task for the agent
    
    A task has:
    - description: What needs to be done
    - agent: Which agent will execute the task
    - expected_output: What the output should look like
    """
    print("=" * 60)
    print("Creating a Simple Research Task")
    print("=" * 60)
    print()
    
    task = Task(
        description="""Research the benefits of using AI agents in business automation.
        Focus on:
        1. Efficiency improvements
        2. Cost savings
        3. Common use cases
        
        Provide a brief summary (3-5 sentences) of your findings.""",
        agent=agent,
        expected_output="A concise summary of AI agent benefits in business automation"
    )
    
    print("✅ Task created successfully!")
    print(f"   Description: {task.description[:80]}...")
    print()
    
    return task


def execute_crew(agent, task):
    """
    Step 4: Execute the task using a Crew
    
    A Crew orchestrates agents and tasks:
    - agents: List of agents in the crew
    - tasks: List of tasks to execute
    - process: How tasks are executed (sequential or hierarchical)
    - verbose: Logging level
    """
    print("=" * 60)
    print("Executing the Crew")
    print("=" * 60)
    print()
    
    # Create a crew with the agent and task
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Starting crew execution...")
    print()
    
    try:
        # Execute the crew
        result = crew.kickoff()
        
        print()
        print("=" * 60)
        print("Execution Complete!")
        print("=" * 60)
        print()
        print("📊 Result:")
        print(result)
        print()
        
        return result
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Error during execution")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Common issues:")
        print("1. Missing OPENAI_API_KEY environment variable")
        print("2. Invalid API key")
        print("3. Network connectivity issues")
        print()
        return None


def main():
    """
    Main function to run Lesson 1
    """
    print()
    print("🎓 Welcome to CrewAI with FastMCP - Lesson 1")
    print()
    
    # Step 1: Setup environment
    env_config = setup_environment()
    
    if not env_config["openai_key"]:
        print("❌ Cannot proceed without OPENAI_API_KEY")
        print("Please set up your environment variables and try again.")
        return
    
    # Step 2: Create agent
    agent = create_basic_agent()
    
    # Step 3: Create task
    task = create_simple_task(agent)
    
    # Step 4: Execute crew
    result = execute_crew(agent, task)
    
    if result:
        print("=" * 60)
        print("🎉 Lesson 1 Complete!")
        print("=" * 60)
        print()
        print("What you learned:")
        print("✅ How to set up environment variables")
        print("✅ How to create a CrewAI agent")
        print("✅ How to define a task")
        print("✅ How to execute a crew")
        print()
        print("Next: Run lesson2_mcp_integration.py to learn about MCP server integration")
        print()
    else:
        print("=" * 60)
        print("⚠️  Lesson 1 encountered errors")
        print("=" * 60)
        print("Please fix the issues above and try again.")
        print()


if __name__ == "__main__":
    main()
