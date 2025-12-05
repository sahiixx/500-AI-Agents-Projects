"""
Dubai Real Estate Lead Generation Workflow - Main Entry Point

This is the main orchestration file that brings together all agents and tasks
to execute the complete lead generation workflow.

Workflow stages:
1. Lead Scraping - Extract leads from multiple sources
2. Verification - Validate property and contact information
3. Qualification - Score and filter leads
4. CRM Integration - Add qualified leads to CRM systems
5. Communication - Send personalized outreach messages
6. Analytics - Generate reports and dashboards
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process
import yaml

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import create_agents
from tasks import create_tasks

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """Load workflow configuration"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    optional_vars = [
        'DUBAI_LAND_DEPT_API_KEY',
        'GOOGLE_SHEETS_CREDENTIALS_FILE',
        'AIRTABLE_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'SMTP_USERNAME',
        'N8N_WEBHOOK_URL'
    ]
    
    print("\n" + "=" * 60)
    print("Environment Configuration Check")
    print("=" * 60)
    
    missing_required = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set (REQUIRED)")
            missing_required.append(var)
    
    print("\nOptional configurations:")
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set (optional, using mock data)")
    
    print("=" * 60 + "\n")
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("Please set them in your .env file and try again.")
        return False
    
    return True


def create_workflow(config):
    """
    Create and configure the workflow crew
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured Crew instance
    """
    logger.info("Creating workflow crew...")
    
    # Create agents
    agents = create_agents(config)
    logger.info(f"Created {len(agents)} agents")
    
    # Create tasks
    tasks = create_tasks(agents, config)
    logger.info(f"Created {len(tasks)} tasks")
    
    # Create crew with sequential process
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    logger.info("Workflow crew created successfully")
    return crew


def run_workflow():
    """
    Main function to run the complete workflow
    """
    print("\n" + "=" * 60)
    print("🏢 Dubai Real Estate Lead Generation Workflow")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    # Check environment
    if not check_environment():
        return
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('dashboards', exist_ok=True)
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        workflow_config = config.get('workflow', {})
        
        print(f"Workflow: {workflow_config.get('name', 'Dubai Real Estate Lead Generation')}")
        print(f"Version: {workflow_config.get('version', '1.0.0')}")
        print(f"Mode: {workflow_config.get('mode', 'continuous')}")
        print()
        
        # Create workflow
        logger.info("Initializing workflow...")
        crew = create_workflow(config)
        
        # Execute workflow
        print("=" * 60)
        print("🚀 Starting Workflow Execution")
        print("=" * 60)
        print()
        
        logger.info("Executing workflow...")
        result = crew.kickoff()
        
        # Display results
        print()
        print("=" * 60)
        print("✅ Workflow Execution Complete!")
        print("=" * 60)
        print()
        print("📊 Final Results:")
        print(result)
        print()
        
        # Log completion
        logger.info("Workflow completed successfully")
        
        print("=" * 60)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Check the 'dashboards/' directory for generated reports")
        print("2. Review the 'logs/workflow.log' file for detailed execution logs")
        print("3. Check your CRM systems for newly added leads")
        print("4. Monitor communication channels for lead responses")
        print()
        
        return result
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        logger.warning("Workflow interrupted by user")
        
    except Exception as e:
        print(f"\n\n❌ Error during workflow execution: {str(e)}")
        logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
        
        print("\nTroubleshooting:")
        print("1. Check that all required environment variables are set")
        print("2. Verify your OpenAI API key is valid")
        print("3. Review the logs/workflow.log file for detailed error information")
        print("4. Ensure all dependencies are installed: pip install -r requirements.txt")
        print()


def run_test_mode():
    """
    Run workflow in test mode with mock data
    """
    print("\n" + "=" * 60)
    print("🧪 Test Mode - Dubai Real Estate Workflow")
    print("=" * 60)
    print()
    
    print("Test mode will:")
    print("- Use mock data for all external API calls")
    print("- Skip actual CRM integrations")
    print("- Skip sending real messages")
    print("- Generate sample analytics")
    print()
    
    # Set test mode environment variable
    os.environ['TEST_MODE'] = 'true'
    
    # Run workflow
    run_workflow()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Dubai Real Estate Lead Generation Workflow'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode with mock data'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom config file'
    )
    
    args = parser.parse_args()
    
    # Override config path if provided
    if args.config:
        os.environ['CONFIG_PATH'] = args.config
    
    # Run in appropriate mode
    if args.test:
        run_test_mode()
    else:
        run_workflow()
