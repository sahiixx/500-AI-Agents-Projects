"""
Task definitions for Dubai Real Estate Lead Generation Workflow

This module defines all tasks for the workflow:
- Lead scraping tasks
- Verification tasks
- Qualification tasks
- CRM integration tasks
- Communication tasks
- Analytics tasks
"""

import yaml
from crewai import Task


def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def create_tasks(agents: dict, config: dict = None):
    """
    Create all tasks for the workflow
    
    Args:
        agents: Dictionary of agent instances
        config: Configuration dictionary (loaded from config.yaml)
        
    Returns:
        List of task instances in execution order
    """
    if config is None:
        config = load_config()
    
    # Get configuration values
    lead_qual = config.get('lead_qualification', {})
    target_areas = config.get('target_areas', [])
    data_sources = config.get('data_sources', {})
    
    # Task 1: Scrape leads from multiple sources
    scraping_task = Task(
        description=f"""Scrape property buyer leads from multiple sources in Dubai.
        
        Target areas: {', '.join(target_areas)}
        
        Data sources to scrape:
        - LinkedIn: Search for property buyers and mortgage inquiries
        - Property Finder: Extract buyer inquiries
        - Bayut: Collect lead information
        - Dubizzle: Gather property inquiries
        
        For each lead, extract:
        - Name
        - Contact information (email, phone)
        - Budget range
        - Preferred areas
        - Property type preferences
        - Number of bedrooms
        - Source platform
        
        Aim to collect at least 50 leads from all sources combined.
        Ensure data quality and avoid duplicates.""",
        agent=agents['lead_scraper'],
        expected_output="A comprehensive list of at least 50 property buyer leads with complete contact information and preferences"
    )
    
    # Task 2: Verify leads and property information
    verification_task = Task(
        description=f"""Verify the authenticity and quality of scraped leads.
        
        For each lead:
        1. Verify property area against Dubai Land Department database
        2. Validate contact information (email format, phone number format)
        3. Check for suspicious or fake data patterns
        4. Verify property types and areas are legitimate
        
        Criteria:
        - Budget range: AED {lead_qual.get('min_budget_aed', 600000):,} - {lead_qual.get('max_budget_aed', 50000000):,}
        - Property types: {', '.join(lead_qual.get('property_types', []))}
        - Bedrooms: {lead_qual.get('bedroom_range', {}).get('min', 1)}-{lead_qual.get('bedroom_range', {}).get('max', 2)} BHK
        
        Mark each lead as verified or unverified.
        Remove leads with invalid contact information.""",
        agent=agents['verification_agent'],
        expected_output="Verified lead list with validation status for each lead, including verification details and any issues found"
    )
    
    # Task 3: Qualify leads based on criteria
    qualification_task = Task(
        description=f"""Qualify and score leads based on predefined criteria.
        
        Qualification criteria:
        - Budget alignment: Does the budget match our target range?
        - Area preference: Is the preferred area in our target list?
        - Property type: Does it match our focus areas?
        - Contact quality: Is the contact information complete and verified?
        - Engagement level: Based on source and inquiry details
        
        Scoring system (0-10):
        - Budget match: 0-3 points
        - Area preference: 0-2 points
        - Property type match: 0-2 points
        - Contact quality: 0-2 points
        - Engagement indicators: 0-1 point
        
        Qualification threshold: Score >= 6
        
        Categorize leads as:
        - Hot (score 8-10): Immediate follow-up
        - Warm (score 6-7): Standard follow-up
        - Cold (score <6): Nurture campaign
        
        Only pass leads with score >= 6 to the next stage.""",
        agent=agents['qualification_agent'],
        expected_output="Qualified lead list with scores and categories, filtered to include only leads scoring 6 or above"
    )
    
    # Task 4: Add qualified leads to CRM
    crm_task = Task(
        description="""Add all qualified leads to CRM systems.
        
        Actions:
        1. Format lead data according to CRM schema
        2. Add leads to Google Sheets (primary CRM)
        3. Sync leads to Airtable (backup CRM)
        4. Ensure all required fields are populated
        5. Add timestamps and source tracking
        
        Required fields for each lead:
        - Name
        - Email
        - Phone
        - Budget
        - Preferred Area
        - Property Type
        - Bedrooms
        - Source
        - Status (new)
        - Qualification Score
        - Verified (true/false)
        - Created Date
        
        Handle errors gracefully and report any failed additions.""",
        agent=agents['crm_agent'],
        expected_output="CRM integration report showing number of leads successfully added to each system, with any errors noted"
    )
    
    # Task 5: Send personalized communications
    communication_task = Task(
        description="""Send personalized outreach messages to qualified leads.
        
        Communication strategy:
        - Hot leads (score 8-10): WhatsApp + Email
        - Warm leads (score 6-7): Email only
        
        Message personalization:
        - Use lead's name
        - Reference their preferred area
        - Mention budget-appropriate properties
        - Include specific property details
        - Add clear call-to-action
        
        Channels:
        1. WhatsApp (via Twilio): For hot leads
        2. Email (via SMTP): For all qualified leads
        3. n8n Webhook: Trigger automation workflows
        
        Track:
        - Messages sent per channel
        - Delivery status
        - Any failures
        
        Respect rate limits and avoid spam.""",
        agent=agents['communication_agent'],
        expected_output="Communication report detailing messages sent via each channel, delivery status, and any issues encountered"
    )
    
    # Task 6: Generate analytics and dashboard
    analytics_task = Task(
        description="""Generate comprehensive analytics and dashboard for the workflow.
        
        Calculate metrics:
        - Total leads found
        - Leads qualified (count and percentage)
        - Conversion rate
        - Follow-up responses
        - Properties in demand (top areas, property types)
        - Average budget
        - Top performing sources
        - Quality metrics (average score, verification rate)
        
        Generate dashboards:
        1. HTML dashboard with visualizations
        2. JSON export for API integration
        3. Summary report
        
        Dashboard should include:
        - Key performance indicators (KPIs)
        - Lead distribution charts
        - Budget analysis
        - Top areas in demand
        - Quality metrics
        - Trend analysis
        
        Save dashboard to 'dashboards/' directory with timestamp.""",
        agent=agents['analytics_agent'],
        expected_output="Analytics report with all calculated metrics and paths to generated dashboard files (HTML and JSON)"
    )
    
    # Return tasks in execution order
    return [
        scraping_task,
        verification_task,
        qualification_task,
        crm_task,
        communication_task,
        analytics_task
    ]


if __name__ == "__main__":
    # Test task creation
    print("Testing task creation...")
    
    # Mock agents for testing
    mock_agents = {
        'lead_scraper': None,
        'verification_agent': None,
        'qualification_agent': None,
        'crm_agent': None,
        'communication_agent': None,
        'analytics_agent': None
    }
    
    try:
        tasks = create_tasks(mock_agents)
        print(f"✅ Created {len(tasks)} tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task.description.split('.')[0]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
