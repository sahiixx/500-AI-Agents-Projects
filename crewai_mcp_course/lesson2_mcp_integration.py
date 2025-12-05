"""
Lesson 2: Integrating MCP Server with CrewAI

This lesson covers:
- Creating custom tools for MCP server access
- Configuring authentication and connection settings
- Using MCP server data in agent tasks
- Handling errors and exceptions

Learning Objectives:
- Build custom CrewAI tools
- Integrate FastMCP server with agents
- Handle API authentication
- Implement error handling and retries
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


class FastMCPTool(BaseTool):
    """
    Custom tool for accessing FastMCP server
    
    This tool demonstrates how to:
    - Create a custom CrewAI tool
    - Make authenticated API requests
    - Handle responses and errors
    - Return structured data to agents
    """
    
    name: str = "FastMCP Data Retriever"
    description: str = (
        "Retrieves data from FastMCP server. "
        "Use this tool to fetch information stored in the MCP server. "
        "Provide a query or data key to retrieve specific information."
    )
    
    def __init__(self):
        super().__init__()
        self.base_url = os.getenv("FASTMCP_URL", "http://localhost:8000")
        self.api_key = os.getenv("FASTMCP_API_KEY", "")
    
    def _run(self, query: str) -> str:
        """
        Execute the tool to retrieve data from MCP server
        
        Args:
            query: The query or data key to retrieve
            
        Returns:
            Retrieved data as a string
        """
        print(f"\n🔍 FastMCP Tool: Retrieving data for query: '{query}'")
        
        try:
            # Prepare request headers
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # Prepare request payload
            payload = {
                "query": query,
                "format": "json"
            }
            
            # Make request to MCP server
            # Note: This is a mock implementation
            # In production, replace with actual MCP server endpoint
            endpoint = f"{self.base_url}/api/query"
            
            print(f"📡 Connecting to: {endpoint}")
            
            # Mock response for demonstration
            # In production, use: response = requests.post(endpoint, json=payload, headers=headers)
            mock_data = self._get_mock_data(query)
            
            print(f"✅ Data retrieved successfully")
            return json.dumps(mock_data, indent=2)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Error connecting to MCP server: {str(e)}"
            print(error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _get_mock_data(self, query: str) -> Dict[str, Any]:
        """
        Generate mock data for demonstration
        
        In production, this would be replaced with actual MCP server responses
        """
        mock_database = {
            "user_preferences": {
                "theme": "dark",
                "language": "en",
                "notifications": True
            },
            "research_findings": {
                "topic": "AI Agents in Business",
                "key_points": [
                    "AI agents can automate repetitive tasks",
                    "Average cost savings of 30-40%",
                    "Improved accuracy and consistency",
                    "24/7 availability"
                ],
                "sources": ["Industry Report 2024", "McKinsey Study"]
            },
            "project_status": {
                "name": "CrewAI Integration",
                "status": "in_progress",
                "completion": 75,
                "next_milestone": "MCP Server Integration"
            }
        }
        
        # Try to find matching data
        query_lower = query.lower()
        for key, value in mock_database.items():
            if key in query_lower or any(word in query_lower for word in key.split('_')):
                return {
                    "query": query,
                    "data": value,
                    "source": "FastMCP Server",
                    "timestamp": "2024-10-28T12:00:00Z"
                }
        
        # Default response if no match found
        return {
            "query": query,
            "data": f"No specific data found for '{query}'. Available keys: {list(mock_database.keys())}",
            "source": "FastMCP Server",
            "timestamp": "2024-10-28T12:00:00Z"
        }


def setup_mcp_integration():
    """
    Step 1: Set up MCP server integration
    """
    print("=" * 60)
    print("LESSON 2: Integrating MCP Server with CrewAI")
    print("=" * 60)
    print()
    
    # Check MCP server configuration
    fastmcp_url = os.getenv("FASTMCP_URL", "http://localhost:8000")
    fastmcp_key = os.getenv("FASTMCP_API_KEY", "")
    
    print("📡 MCP Server Configuration:")
    print(f"   URL: {fastmcp_url}")
    print(f"   API Key: {'✅ Set' if fastmcp_key else '⚠️  Not set (using mock data)'}")
    print()
    
    return {
        "url": fastmcp_url,
        "api_key": fastmcp_key
    }


def create_mcp_enabled_agent(mcp_tool):
    """
    Step 2: Create an agent with MCP server access
    
    This agent can use the FastMCP tool to retrieve data
    """
    print("=" * 60)
    print("Creating MCP-Enabled Research Agent")
    print("=" * 60)
    print()
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )
    
    researcher = Agent(
        role="MCP Research Analyst",
        goal="Gather information from MCP server and analyze it",
        backstory="""You are a research analyst with access to a FastMCP server
        containing valuable data and insights. You know how to query the server
        effectively and interpret the results to provide meaningful analysis.""",
        tools=[mcp_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    print("✅ MCP-Enabled Agent created successfully!")
    print(f"   Role: {researcher.role}")
    print(f"   Tools: {[tool.name for tool in researcher.tools]}")
    print()
    
    return researcher


def create_mcp_task(agent):
    """
    Step 3: Create a task that uses MCP server data
    """
    print("=" * 60)
    print("Creating MCP Data Retrieval Task")
    print("=" * 60)
    print()
    
    task = Task(
        description="""Use the FastMCP Data Retriever tool to fetch research findings
        about AI agents in business. Analyze the retrieved data and provide:
        
        1. A summary of the key findings
        2. The most important benefits mentioned
        3. Your assessment of the data quality
        
        Make sure to use the tool to retrieve the data first, then analyze it.""",
        agent=agent,
        expected_output="Analysis of MCP server data about AI agents in business"
    )
    
    print("✅ Task created successfully!")
    print(f"   Agent will use: {agent.tools[0].name}")
    print()
    
    return task


def execute_mcp_crew(agent, task):
    """
    Step 4: Execute the crew with MCP integration
    """
    print("=" * 60)
    print("Executing MCP-Enabled Crew")
    print("=" * 60)
    print()
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Starting crew execution with MCP server access...")
    print()
    
    try:
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
        print("Troubleshooting:")
        print("1. Check OPENAI_API_KEY is set")
        print("2. Verify FASTMCP_URL is correct")
        print("3. Ensure FASTMCP_API_KEY is valid (if required)")
        print("4. Check network connectivity")
        print()
        return None


def demonstrate_error_handling():
    """
    Step 5: Demonstrate error handling with MCP tools
    """
    print("=" * 60)
    print("Demonstrating Error Handling")
    print("=" * 60)
    print()
    
    mcp_tool = FastMCPTool()
    
    # Test successful query
    print("Test 1: Valid query")
    result1 = mcp_tool._run("research_findings")
    print(f"Result: {result1[:100]}...")
    print()
    
    # Test query with no results
    print("Test 2: Query with no specific match")
    result2 = mcp_tool._run("nonexistent_data")
    print(f"Result: {result2[:100]}...")
    print()
    
    print("✅ Error handling demonstration complete")
    print()


def main():
    """
    Main function to run Lesson 2
    """
    print()
    print("🎓 Welcome to CrewAI with FastMCP - Lesson 2")
    print()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        print("Please set it in your .env file and try again.")
        return
    
    # Step 1: Setup MCP integration
    mcp_config = setup_mcp_integration()
    
    # Step 2: Create MCP tool
    print("=" * 60)
    print("Creating FastMCP Tool")
    print("=" * 60)
    print()
    mcp_tool = FastMCPTool()
    print(f"✅ Tool created: {mcp_tool.name}")
    print(f"   Description: {mcp_tool.description[:60]}...")
    print()
    
    # Step 3: Create MCP-enabled agent
    agent = create_mcp_enabled_agent(mcp_tool)
    
    # Step 4: Create task
    task = create_mcp_task(agent)
    
    # Step 5: Demonstrate error handling
    demonstrate_error_handling()
    
    # Step 6: Execute crew
    result = execute_mcp_crew(agent, task)
    
    if result:
        print("=" * 60)
        print("🎉 Lesson 2 Complete!")
        print("=" * 60)
        print()
        print("What you learned:")
        print("✅ How to create custom CrewAI tools")
        print("✅ How to integrate FastMCP server")
        print("✅ How to handle authentication")
        print("✅ How to implement error handling")
        print()
        print("Next: Run lesson3_advanced_patterns.py for multi-agent workflows")
        print()
    else:
        print("=" * 60)
        print("⚠️  Lesson 2 encountered errors")
        print("=" * 60)
        print("Please fix the issues above and try again.")
        print()


if __name__ == "__main__":
    main()
