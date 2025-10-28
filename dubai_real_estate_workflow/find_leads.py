#!/usr/bin/env python3
"""
Dubai Real Estate Lead Generation Script
Finds and qualifies property buyers in UAE
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any
import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dubai_real_estate_workflow.tools.scraping_tools import (
    LinkedInScraperTool,
    PropertyFinderScraperTool,
    BayutScraperTool,
    DubizzleScraperTool
)
from dubai_real_estate_workflow.tools.verification_tools import (
    DubaiLandDeptVerificationTool,
    ContactVerificationTool
)
from dubai_real_estate_workflow.tools.crm_tools import (
    GoogleSheetsTool,
    AirtableTool
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DubaiRealEstateLeadFinder:
    """Main class for finding and qualifying property buyer leads in UAE"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the lead finder with configuration"""
        load_dotenv()
        
        # Load configuration
        config_file = os.path.join(
            os.path.dirname(__file__), 
            config_path
        )
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize tools
        self.linkedin_scraper = LinkedInScraperTool()
        self.property_finder_scraper = PropertyFinderScraperTool()
        self.bayut_scraper = BayutScraperTool()
        self.dubizzle_scraper = DubizzleScraperTool()
        self.verification_tool = ContactVerificationTool()
        self.property_verification = DubaiLandDeptVerificationTool()
        self.google_sheets = GoogleSheetsTool()
        self.airtable = AirtableTool()
        
        self.all_leads = []
        self.qualified_leads = []
        
    def scrape_all_sources(self) -> List[Dict[str, Any]]:
        """Scrape leads from all configured sources"""
        logger.info("=" * 80)
        logger.info("STARTING LEAD GENERATION FOR UAE PROPERTY BUYERS")
        logger.info("=" * 80)
        
        all_leads = []
        
        # Scrape LinkedIn
        if self.config['data_sources']['linkedin']['enabled']:
            logger.info("\n📱 Scraping LinkedIn...")
            keywords = self.config['data_sources']['linkedin']['search_keywords']
            max_results = self.config['data_sources']['linkedin']['max_results_per_search']
            linkedin_leads = self.linkedin_scraper._run(keywords, max_results)
            all_leads.extend(linkedin_leads)
            logger.info(f"✅ Found {len(linkedin_leads)} leads from LinkedIn")
        
        # Scrape Property Finder
        if self.config['data_sources']['property_finder']['enabled']:
            logger.info("\n🏢 Scraping Property Finder...")
            pf_leads = self.property_finder_scraper._run()
            all_leads.extend(pf_leads)
            logger.info(f"✅ Found {len(pf_leads)} leads from Property Finder")
        
        # Scrape Bayut
        if self.config['data_sources']['bayut']['enabled']:
            logger.info("\n🏠 Scraping Bayut...")
            bayut_leads = self.bayut_scraper._run()
            all_leads.extend(bayut_leads)
            logger.info(f"✅ Found {len(bayut_leads)} leads from Bayut")
        
        # Scrape Dubizzle
        if self.config['data_sources']['dubizzle']['enabled']:
            logger.info("\n📋 Scraping Dubizzle...")
            dubizzle_leads = self.dubizzle_scraper._run()
            all_leads.extend(dubizzle_leads)
            logger.info(f"✅ Found {len(dubizzle_leads)} leads from Dubizzle")
        
        self.all_leads = all_leads
        logger.info(f"\n📊 TOTAL LEADS FOUND: {len(all_leads)}")
        return all_leads
    
    def verify_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verify contact information for all leads"""
        logger.info("\n" + "=" * 80)
        logger.info("VERIFYING LEAD CONTACT INFORMATION")
        logger.info("=" * 80)
        
        verified_leads = []
        
        for idx, lead in enumerate(leads, 1):
            logger.info(f"\n🔍 Verifying lead {idx}/{len(leads)}: {lead.get('name', 'Unknown')}")
            
            # Verify contact information
            verification_result = self.verification_tool._run(
                email=lead.get('email'),
                phone=lead.get('phone'),
                name=lead.get('name')
            )
            
            lead['verified'] = verification_result['overall_valid']
            lead['email_valid'] = verification_result.get('email_valid', False)
            lead['phone_valid'] = verification_result.get('phone_valid', False)
            lead['name_valid'] = verification_result.get('name_valid', False)
            
            # Verify property area if available
            if lead.get('preferred_area'):
                property_verification = self.property_verification._run(
                    property_area=lead['preferred_area'],
                    property_type=lead.get('property_type', 'apartment')
                )
                lead['area_verified'] = property_verification['verified']
            
            if lead['verified']:
                verified_leads.append(lead)
                logger.info(f"✅ Lead verified successfully")
            else:
                logger.info(f"❌ Lead verification failed")
        
        logger.info(f"\n📊 VERIFIED LEADS: {len(verified_leads)}/{len(leads)}")
        return verified_leads
    
    def qualify_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Qualify leads based on budget and preferences"""
        logger.info("\n" + "=" * 80)
        logger.info("QUALIFYING LEADS BASED ON CRITERIA")
        logger.info("=" * 80)
        
        qualification_config = self.config['lead_qualification']
        min_budget = qualification_config['min_budget_aed']
        max_budget = qualification_config['max_budget_aed']
        target_areas = self.config['target_areas']
        
        logger.info(f"\n📋 Qualification Criteria:")
        logger.info(f"   • Budget Range: AED {min_budget:,} - {max_budget:,}")
        logger.info(f"   • Target Areas: {', '.join(target_areas[:3])}...")
        logger.info(f"   • Property Types: {', '.join(qualification_config['property_types'])}")
        
        qualified_leads = []
        
        for idx, lead in enumerate(leads, 1):
            logger.info(f"\n🎯 Qualifying lead {idx}/{len(leads)}: {lead.get('name', 'Unknown')}")
            
            qualification_score = 0
            reasons = []
            
            # Check budget
            budget = lead.get('budget', 0)
            if min_budget <= budget <= max_budget:
                qualification_score += 30
                reasons.append(f"✓ Budget in range (AED {budget:,})")
            else:
                reasons.append(f"✗ Budget out of range (AED {budget:,})")
            
            # Check preferred area
            preferred_area = lead.get('preferred_area', '')
            if any(area.lower() in preferred_area.lower() for area in target_areas):
                qualification_score += 25
                reasons.append(f"✓ Target area ({preferred_area})")
            else:
                reasons.append(f"✗ Non-target area ({preferred_area})")
            
            # Check property type
            property_type = lead.get('property_type', '')
            if property_type in qualification_config['property_types']:
                qualification_score += 20
                reasons.append(f"✓ Desired property type ({property_type})")
            
            # Check verification status
            if lead.get('verified', False):
                qualification_score += 15
                reasons.append("✓ Contact verified")
            
            # Check area verification
            if lead.get('area_verified', False):
                qualification_score += 10
                reasons.append("✓ Area verified")
            
            lead['qualification_score'] = qualification_score
            lead['qualification_reasons'] = reasons
            lead['status'] = 'qualified' if qualification_score >= 50 else 'unqualified'
            
            # Log qualification details
            for reason in reasons:
                logger.info(f"   {reason}")
            logger.info(f"   📊 Score: {qualification_score}/100")
            
            if qualification_score >= 50:
                qualified_leads.append(lead)
                logger.info(f"   ✅ QUALIFIED")
            else:
                logger.info(f"   ❌ NOT QUALIFIED")
        
        self.qualified_leads = qualified_leads
        logger.info(f"\n📊 QUALIFIED LEADS: {len(qualified_leads)}/{len(leads)}")
        return qualified_leads
    
    def export_leads(self, leads: List[Dict[str, Any]], export_to: str = "both"):
        """Export qualified leads to CRM systems"""
        logger.info("\n" + "=" * 80)
        logger.info("EXPORTING QUALIFIED LEADS TO CRM")
        logger.info("=" * 80)
        
        if not leads:
            logger.warning("⚠️  No leads to export")
            return
        
        # Export to Google Sheets
        if export_to in ["google_sheets", "both"]:
            logger.info("\n📊 Exporting to Google Sheets...")
            result = self.google_sheets._run(leads)
            if result['success']:
                logger.info(f"✅ Successfully exported {result['added_count']} leads to Google Sheets")
            else:
                logger.error(f"❌ Failed to export to Google Sheets: {result.get('error')}")
        
        # Export to Airtable
        if export_to in ["airtable", "both"]:
            logger.info("\n📋 Exporting to Airtable...")
            result = self.airtable._run(leads)
            if result['success']:
                logger.info(f"✅ Successfully exported {result['added_count']} leads to Airtable")
            else:
                logger.error(f"❌ Failed to export to Airtable: {result.get('error')}")
    
    def generate_report(self):
        """Generate a summary report of the lead generation process"""
        logger.info("\n" + "=" * 80)
        logger.info("LEAD GENERATION SUMMARY REPORT")
        logger.info("=" * 80)
        
        logger.info(f"\n📊 Statistics:")
        logger.info(f"   • Total Leads Found: {len(self.all_leads)}")
        logger.info(f"   • Qualified Leads: {len(self.qualified_leads)}")
        logger.info(f"   • Qualification Rate: {len(self.qualified_leads)/len(self.all_leads)*100:.1f}%" if self.all_leads else "   • Qualification Rate: 0%")
        
        # Source breakdown
        if self.all_leads:
            logger.info(f"\n📱 Leads by Source:")
            sources = {}
            for lead in self.all_leads:
                source = lead.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            for source, count in sources.items():
                logger.info(f"   • {source}: {count}")
        
        # Top areas
        if self.qualified_leads:
            logger.info(f"\n🏙️  Top Preferred Areas:")
            areas = {}
            for lead in self.qualified_leads:
                area = lead.get('preferred_area', 'Unknown')
                areas[area] = areas.get(area, 0) + 1
            
            for area, count in sorted(areas.items(), key=lambda x: x[1], reverse=True)[:5]:
                logger.info(f"   • {area}: {count} leads")
        
        # Budget analysis
        if self.qualified_leads:
            budgets = [lead.get('budget', 0) for lead in self.qualified_leads if lead.get('budget')]
            if budgets:
                avg_budget = sum(budgets) / len(budgets)
                logger.info(f"\n💰 Budget Analysis:")
                logger.info(f"   • Average Budget: AED {avg_budget:,.0f}")
                logger.info(f"   • Min Budget: AED {min(budgets):,}")
                logger.info(f"   • Max Budget: AED {max(budgets):,}")
        
        logger.info("\n" + "=" * 80)
        logger.info(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80 + "\n")
    
    def run(self, export_to: str = "both"):
        """Run the complete lead generation workflow"""
        try:
            # Step 1: Scrape all sources
            all_leads = self.scrape_all_sources()
            
            if not all_leads:
                logger.warning("⚠️  No leads found from any source")
                return
            
            # Step 2: Verify leads
            verified_leads = self.verify_leads(all_leads)
            
            if not verified_leads:
                logger.warning("⚠️  No leads passed verification")
                return
            
            # Step 3: Qualify leads
            qualified_leads = self.qualify_leads(verified_leads)
            
            if not qualified_leads:
                logger.warning("⚠️  No leads met qualification criteria")
                return
            
            # Step 4: Export leads
            self.export_leads(qualified_leads, export_to)
            
            # Step 5: Generate report
            self.generate_report()
            
            logger.info("✅ Lead generation workflow completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error in lead generation workflow: {str(e)}")
            raise


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("🏢 DUBAI REAL ESTATE LEAD GENERATION SYSTEM")
    print("=" * 80 + "\n")
    
    # Initialize and run lead finder
    lead_finder = DubaiRealEstateLeadFinder()
    lead_finder.run(export_to="both")
    
    print("\n✅ Process completed! Check the logs above for detailed results.\n")


if __name__ == "__main__":
    main()
