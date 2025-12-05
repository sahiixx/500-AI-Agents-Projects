"""
Agent definitions for Dubai Real Estate Lead Generation Workflow

This module defines all agents used in the workflow:
- Lead Scraper Agent
- Verification Agent
- Qualification Agent
- CRM Integration Agent
- Communication Agent
- Analytics Agent
"""

import yaml
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import (
    LinkedInScraperTool,
    PropertyFinderScraperTool,
    BayutScraperTool,
    DubizzleScraperTool,
    DubaiLandDeptVerificationTool,
    ContactVerificationTool,
    GoogleSheetsTool,
    AirtableTool,
    TwilioWhatsAppTool,
    EmailTool,
    N8NWebhookTool,
    DashboardGeneratorTool,
    MetricsCalculatorTool
)


def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def create_agents(config: dict = None):
    """
    Create all agents for the workflow
    
    Args:
        config: Configuration dictionary (loaded from config.yaml)
        
    Returns:
        Dictionary of agent instances
    """
    if config is None:
        config = load_config()
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )
    
    # Initialize tools
    linkedin_tool = LinkedInScraperTool()
    property_finder_tool = PropertyFinderScraperTool()
    bayut_tool = BayutScraperTool()
    dubizzle_tool = DubizzleScraperTool()
    
    dubai_land_tool = DubaiLandDeptVerificationTool()
    contact_verification_tool = ContactVerificationTool()
    
    google_sheets_tool = GoogleSheetsTool()
    airtable_tool = AirtableTool()
    
    whatsapp_tool = TwilioWhatsAppTool()
    email_tool = EmailTool()
    n8n_tool = N8NWebhookTool()
    
    metrics_tool = MetricsCalculatorTool()
    dashboard_tool = DashboardGeneratorTool()
    
    # Get agent configurations
    agent_configs = config.get('agents', {})
    
    # 1. Lead Scraper Agent
    scraper_config = agent_configs.get('lead_scraper', {})
    lead_scraper = Agent(
        role=scraper_config.get('role', 'Lead Scraper Agent'),
        goal=scraper_config.get('goal', 'Extract high-quality property buyer leads from multiple sources'),
        backstory=scraper_config.get('backstory', 'Expert web scraper specialized in Dubai real estate market'),
        tools=[linkedin_tool, property_finder_tool, bayut_tool, dubizzle_tool],
        verbose=scraper_config.get('verbose', True),
        allow_delegation=scraper_config.get('allow_delegation', False),
        llm=llm
    )
    
    # 2. Verification Agent
    verification_config = agent_configs.get('verification_agent', {})
    verification_agent = Agent(
        role=verification_config.get('role', 'Property Verification Agent'),
        goal=verification_config.get('goal', 'Verify property listings and validate lead authenticity'),
        backstory=verification_config.get('backstory', 'Dubai Land Department specialist with deep knowledge of property regulations'),
        tools=[dubai_land_tool, contact_verification_tool],
        verbose=verification_config.get('verbose', True),
        allow_delegation=verification_config.get('allow_delegation', False),
        llm=llm
    )
    
    # 3. Qualification Agent
    qualification_config = agent_configs.get('qualification_agent', {})
    qualification_agent = Agent(
        role=qualification_config.get('role', 'Lead Qualification Agent'),
        goal=qualification_config.get('goal', 'Filter and qualify leads based on predefined criteria'),
        backstory=qualification_config.get('backstory', 'Senior real estate analyst with expertise in lead scoring'),
        verbose=qualification_config.get('verbose', True),
        allow_delegation=qualification_config.get('allow_delegation', False),
        llm=llm
    )
    
    # 4. CRM Integration Agent
    crm_config = agent_configs.get('crm_integration_agent', {})
    crm_agent = Agent(
        role=crm_config.get('role', 'CRM Integration Agent'),
        goal=crm_config.get('goal', 'Seamlessly add qualified leads to CRM systems'),
        backstory=crm_config.get('backstory', 'CRM specialist with expertise in data integration'),
        tools=[google_sheets_tool, airtable_tool],
        verbose=crm_config.get('verbose', True),
        allow_delegation=crm_config.get('allow_delegation', False),
        llm=llm
    )
    
    # 5. Communication Agent
    communication_config = agent_configs.get('communication_agent', {})
    communication_agent = Agent(
        role=communication_config.get('role', 'Communication Agent'),
        goal=communication_config.get('goal', 'Send personalized messages to qualified leads'),
        backstory=communication_config.get('backstory', 'Marketing automation expert specializing in personalized outreach'),
        tools=[whatsapp_tool, email_tool, n8n_tool],
        verbose=communication_config.get('verbose', True),
        allow_delegation=communication_config.get('allow_delegation', False),
        llm=llm
    )
    
    # 6. Analytics Agent
    analytics_config = agent_configs.get('analytics_agent', {})
    analytics_agent = Agent(
        role=analytics_config.get('role', 'Analytics & Reporting Agent'),
        goal=analytics_config.get('goal', 'Generate comprehensive dashboards and insights'),
        backstory=analytics_config.get('backstory', 'Data analyst with expertise in real estate market trends'),
        tools=[metrics_tool, dashboard_tool],
        verbose=analytics_config.get('verbose', True),
        allow_delegation=analytics_config.get('allow_delegation', False),
        llm=llm
    )
    
    return {
        'lead_scraper': lead_scraper,
        'verification_agent': verification_agent,
        'qualification_agent': qualification_agent,
        'crm_agent': crm_agent,
        'communication_agent': communication_agent,
        'analytics_agent': analytics_agent
    }


if __name__ == "__main__":
    # Test agent creation
    print("Creating agents...")
    agents = create_agents()
    print(f"✅ Created {len(agents)} agents:")
    for name, agent in agents.items():
        print(f"   - {name}: {agent.role}")
