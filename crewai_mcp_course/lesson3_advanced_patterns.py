"""
Lesson 3: Advanced CrewAI Patterns with MCP Server

This lesson covers:
- Implementing multi-agent workflows
- Using hierarchical processes
- Sharing data between agents through the MCP server
- Storing and retrieving research findings
- Implementing quality assurance processes

Learning Objectives:
- Design complex multi-agent systems
- Implement agent collaboration patterns
- Use MCP server for data persistence
- Create hierarchical agent workflows
- Implement review and feedback loops
"""

import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


class MCPStorageTool(BaseTool):
    """
    Tool for storing data in MCP server
    
    Allows agents to persist their findings and share data
    """
    
    name: str = "MCP Data Storage"
    description: str = (
        "Stores data in the FastMCP server for persistence and sharing. "
        "Use this to save research findings, analysis results, or any data "
        "that needs to be accessed by other agents or retrieved later."
    )
    
    def __init__(self):
        super().__init__()
        self.base_url = os.getenv("FASTMCP_URL", "http://localhost:8000")
        self.api_key = os.getenv("FASTMCP_API_KEY", "")
        self.storage = {}  # Mock storage for demonstration
    
    def _run(self, key: str, data: str) -> str:
        """
        Store data in MCP server
        
        Args:
            key: Storage key/identifier
            data: Data to store (as string)
            
        Returns:
            Confirmation message
        """
        print(f"\n💾 Storing data with key: '{key}'")
        
        try:
            # Mock storage implementation
            # In production, make POST request to MCP server
            self.storage[key] = {
                "data": data,
                "timestamp": "2024-10-28T12:00:00Z",
                "stored_by": "MCP Storage Tool"
            }
            
            print(f"✅ Data stored successfully")
            return f"Successfully stored data with key '{key}'"
            
        except Exception as e:
            error_msg = f"❌ Error storing data: {str(e)}"
            print(error_msg)
            return error_msg


class MCPRetrievalTool(BaseTool):
    """
    Tool for retrieving data from MCP server
    
    Allows agents to access data stored by other agents
    """
    
    name: str = "MCP Data Retrieval"
    description: str = (
        "Retrieves data from the FastMCP server. "
        "Use this to access research findings, analysis results, or any data "
        "that was previously stored by other agents."
    )
    
    def __init__(self, storage_tool: MCPStorageTool):
        super().__init__()
        self.base_url = os.getenv("FASTMCP_URL", "http://localhost:8000")
        self.api_key = os.getenv("FASTMCP_API_KEY", "")
        self.storage_tool = storage_tool  # Share storage with storage tool
    
    def _run(self, key: str) -> str:
        """
        Retrieve data from MCP server
        
        Args:
            key: Storage key/identifier
            
        Returns:
            Retrieved data as string
        """
        print(f"\n🔍 Retrieving data with key: '{key}'")
        
        try:
            # Mock retrieval implementation
            # In production, make GET request to MCP server
            if key in self.storage_tool.storage:
                data = self.storage_tool.storage[key]
                print(f"✅ Data retrieved successfully")
                return json.dumps(data, indent=2)
            else:
                msg = f"No data found for key '{key}'"
                print(f"⚠️  {msg}")
                return msg
            
        except Exception as e:
            error_msg = f"❌ Error retrieving data: {str(e)}"
            print(error_msg)
            return error_msg


def create_research_agent(storage_tool):
    """
    Create a researcher agent that stores findings in MCP server
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Conduct thorough research and store findings in MCP server",
        backstory="""You are a senior research analyst with expertise in technology
        and business automation. You conduct comprehensive research and always store
        your findings in the MCP server so other team members can access them.""",
        tools=[storage_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return researcher


def create_writer_agent(retrieval_tool):
    """
    Create a writer agent that retrieves data from MCP server
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    
    writer = Agent(
        role="Technical Writer",
        goal="Create well-structured reports based on research findings",
        backstory="""You are an experienced technical writer who excels at
        transforming research data into clear, engaging reports. You retrieve
        research findings from the MCP server and craft comprehensive documents.""",
        tools=[retrieval_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return writer


def create_reviewer_agent():
    """
    Create a reviewer agent for quality assurance
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    
    reviewer = Agent(
        role="Quality Assurance Reviewer",
        goal="Review reports for accuracy, clarity, and completeness",
        backstory="""You are a meticulous quality assurance specialist with high
        standards. You review all reports to ensure they meet quality criteria,
        are factually accurate, and are well-structured. You provide constructive
        feedback for improvements.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return reviewer


def create_research_task(researcher):
    """
    Task for researcher to gather and store information
    """
    task = Task(
        description="""Research the following topic: 'Benefits of Multi-Agent Systems in Business'
        
        Focus on:
        1. Efficiency improvements from agent collaboration
        2. Scalability advantages
        3. Real-world use cases
        4. Implementation challenges
        
        After completing your research, use the MCP Data Storage tool to store your
        findings with the key 'multi_agent_research'. Format your findings as a
        structured summary with clear sections.""",
        agent=researcher,
        expected_output="Research findings stored in MCP server with key 'multi_agent_research'"
    )
    
    return task


def create_writing_task(writer):
    """
    Task for writer to retrieve data and create report
    """
    task = Task(
        description="""Retrieve the research findings from the MCP server using the key
        'multi_agent_research'. Based on these findings, write a comprehensive report
        titled 'Multi-Agent Systems in Business: A Comprehensive Analysis'.
        
        Your report should include:
        1. Executive Summary
        2. Key Benefits (with specific examples)
        3. Use Cases
        4. Implementation Considerations
        5. Conclusion
        
        Make the report professional, well-structured, and easy to understand.""",
        agent=writer,
        expected_output="A comprehensive report based on retrieved research findings"
    )
    
    return task


def create_review_task(reviewer):
    """
    Task for reviewer to assess the report quality
    """
    task = Task(
        description="""Review the report created by the Technical Writer.
        
        Evaluate the report on:
        1. Accuracy - Are the facts correct and well-supported?
        2. Clarity - Is the writing clear and easy to understand?
        3. Completeness - Does it cover all required sections?
        4. Structure - Is it well-organized and logical?
        5. Professional Quality - Does it meet professional standards?
        
        Provide:
        - An overall quality score (1-10)
        - Specific strengths
        - Areas for improvement
        - Recommendation (Approve / Revise / Reject)""",
        agent=reviewer,
        expected_output="Quality assessment with score, feedback, and recommendation"
    )
    
    return task


def demonstrate_sequential_workflow():
    """
    Demonstrate a sequential multi-agent workflow
    """
    print("=" * 60)
    print("LESSON 3: Advanced Multi-Agent Patterns")
    print("=" * 60)
    print()
    print("Pattern 1: Sequential Workflow with Data Sharing")
    print("=" * 60)
    print()
    
    # Create shared tools
    storage_tool = MCPStorageTool()
    retrieval_tool = MCPRetrievalTool(storage_tool)
    
    # Create agents
    print("Creating agents...")
    researcher = create_research_agent(storage_tool)
    writer = create_writer_agent(retrieval_tool)
    reviewer = create_reviewer_agent()
    print(f"✅ Created 3 agents: Researcher, Writer, Reviewer")
    print()
    
    # Create tasks
    print("Creating tasks...")
    research_task = create_research_task(researcher)
    writing_task = create_writing_task(writer)
    review_task = create_review_task(reviewer)
    print(f"✅ Created 3 sequential tasks")
    print()
    
    # Create crew with sequential process
    print("Creating crew with sequential process...")
    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research_task, writing_task, review_task],
        process=Process.sequential,
        verbose=True
    )
    print(f"✅ Crew created")
    print()
    
    # Execute
    print("=" * 60)
    print("Executing Sequential Workflow")
    print("=" * 60)
    print()
    print("Flow: Researcher → Writer → Reviewer")
    print()
    
    try:
        result = crew.kickoff()
        
        print()
        print("=" * 60)
        print("Sequential Workflow Complete!")
        print("=" * 60)
        print()
        print("📊 Final Result:")
        print(result)
        print()
        
        return result
        
    except Exception as e:
        print()
        print(f"❌ Error: {str(e)}")
        print()
        return None


def demonstrate_hierarchical_workflow():
    """
    Demonstrate a hierarchical workflow with a manager agent
    """
    print("=" * 60)
    print("Pattern 2: Hierarchical Workflow")
    print("=" * 60)
    print()
    
    llm = ChatOpenAI(model="gpt-4", temperature=0.5)
    
    # Create manager agent
    manager = Agent(
        role="Project Manager",
        goal="Coordinate the team to produce high-quality research reports",
        backstory="""You are an experienced project manager who coordinates
        research, writing, and review activities. You delegate tasks effectively
        and ensure the team works efficiently toward the goal.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
    
    # Create worker agents
    storage_tool = MCPStorageTool()
    retrieval_tool = MCPRetrievalTool(storage_tool)
    
    researcher = create_research_agent(storage_tool)
    writer = create_writer_agent(retrieval_tool)
    reviewer = create_reviewer_agent()
    
    # Create a high-level task for the manager
    manager_task = Task(
        description="""Coordinate the team to produce a comprehensive report on
        'Multi-Agent Systems in Business'. Ensure the research is thorough,
        the writing is professional, and the quality is high.
        
        Delegate tasks appropriately and ensure smooth collaboration.""",
        agent=manager,
        expected_output="A high-quality, reviewed report on multi-agent systems"
    )
    
    # Create hierarchical crew
    crew = Crew(
        agents=[manager, researcher, writer, reviewer],
        tasks=[manager_task],
        process=Process.hierarchical,
        verbose=True,
        manager_llm=llm
    )
    
    print("✅ Hierarchical crew created with manager")
    print(f"   Manager: {manager.role}")
    print(f"   Team: {researcher.role}, {writer.role}, {reviewer.role}")
    print()
    
    print("=" * 60)
    print("Executing Hierarchical Workflow")
    print("=" * 60)
    print()
    print("Flow: Manager delegates to → Researcher, Writer, Reviewer")
    print()
    
    try:
        result = crew.kickoff()
        
        print()
        print("=" * 60)
        print("Hierarchical Workflow Complete!")
        print("=" * 60)
        print()
        print("📊 Final Result:")
        print(result)
        print()
        
        return result
        
    except Exception as e:
        print()
        print(f"❌ Error: {str(e)}")
        print("Note: Hierarchical process requires proper OpenAI API access")
        print()
        return None


def main():
    """
    Main function to run Lesson 3
    """
    print()
    print("🎓 Welcome to CrewAI with FastMCP - Lesson 3")
    print()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        print("Please set it in your .env file and try again.")
        return
    
    # Demonstrate sequential workflow
    print("\n" + "=" * 60)
    print("DEMONSTRATION 1: Sequential Multi-Agent Workflow")
    print("=" * 60 + "\n")
    
    result1 = demonstrate_sequential_workflow()
    
    # Demonstrate hierarchical workflow
    if result1:
        print("\n" + "=" * 60)
        print("DEMONSTRATION 2: Hierarchical Multi-Agent Workflow")
        print("=" * 60 + "\n")
        
        result2 = demonstrate_hierarchical_workflow()
    
    # Summary
    print()
    print("=" * 60)
    print("🎉 Lesson 3 Complete!")
    print("=" * 60)
    print()
    print("What you learned:")
    print("✅ Multi-agent collaboration patterns")
    print("✅ Sequential workflow with data sharing")
    print("✅ Hierarchical workflow with manager delegation")
    print("✅ Using MCP server for agent communication")
    print("✅ Implementing review and feedback loops")
    print()
    print("=" * 60)
    print("🎓 Course Complete!")
    print("=" * 60)
    print()
    print("You now know how to:")
    print("• Set up CrewAI agents and tasks")
    print("• Integrate FastMCP server with custom tools")
    print("• Build complex multi-agent workflows")
    print("• Implement data sharing between agents")
    print("• Use both sequential and hierarchical processes")
    print()
    print("Next steps:")
    print("• Explore the dubai_real_estate_workflow for a real-world example")
    print("• Build your own multi-agent system")
    print("• Experiment with different agent roles and tools")
    print()


if __name__ == "__main__":
    main()
