"""
Analytics and reporting tools for generating dashboards and calculating metrics
"""

import os
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter
from crewai_tools import BaseTool

logger = logging.getLogger(__name__)


class MetricsCalculatorTool(BaseTool):
    name: str = "Metrics Calculator"
    description: str = (
        "Calculates key performance metrics from lead data. "
        "Provides insights on conversion rates, lead quality, and trends."
    )
    
    def _run(self, leads: List[Dict[str, Any]], historical_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate metrics from lead data
        
        Args:
            leads: List of lead dictionaries
            historical_data: Optional historical data for trend analysis
            
        Returns:
            Dictionary containing calculated metrics
        """
        try:
            logger.info(f"Calculating metrics for {len(leads)} leads")
            
            if not leads:
                return {
                    "success": False,
                    "error": "No leads provided for analysis",
                    "metrics": {}
                }
            
            # Basic counts
            total_leads = len(leads)
            qualified_leads = sum(1 for lead in leads if lead.get('verified', False))
            
            # Source distribution
            sources = [lead.get('source', 'Unknown') for lead in leads]
            source_distribution = dict(Counter(sources))
            
            # Area preferences
            areas = [lead.get('preferred_area', 'Unknown') for lead in leads]
            area_distribution = dict(Counter(areas))
            top_areas = sorted(area_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Budget analysis
            budgets = [lead.get('budget', 0) for lead in leads if lead.get('budget')]
            average_budget = sum(budgets) / len(budgets) if budgets else 0
            min_budget = min(budgets) if budgets else 0
            max_budget = max(budgets) if budgets else 0
            
            # Property type preferences
            property_types = [lead.get('property_type', 'Unknown') for lead in leads]
            property_type_distribution = dict(Counter(property_types))
            
            # Bedroom preferences
            bedrooms = [lead.get('bedrooms', 0) for lead in leads if lead.get('bedrooms')]
            bedroom_distribution = dict(Counter(bedrooms))
            
            # Qualification scores
            scores = [lead.get('qualification_score', 0) for lead in leads if lead.get('qualification_score')]
            average_score = sum(scores) / len(scores) if scores else 0
            
            # Status distribution
            statuses = [lead.get('status', 'new') for lead in leads]
            status_distribution = dict(Counter(statuses))
            
            # Conversion rate (if historical data provided)
            conversion_rate = 0
            if historical_data and 'total_conversions' in historical_data:
                total_conversions = historical_data.get('total_conversions', 0)
                conversion_rate = (total_conversions / total_leads * 100) if total_leads > 0 else 0
            
            # Response rate (mock calculation)
            follow_up_responses = sum(1 for lead in leads if lead.get('responded', False))
            response_rate = (follow_up_responses / total_leads * 100) if total_leads > 0 else 0
            
            # Properties in demand (based on inquiries)
            properties_in_demand = {
                "high_demand_areas": [area for area, count in top_areas[:3]],
                "popular_property_types": list(property_type_distribution.keys())[:3],
                "preferred_bedrooms": list(bedroom_distribution.keys())[:3]
            }
            
            metrics = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_leads_found": total_leads,
                    "leads_qualified": qualified_leads,
                    "qualification_rate": (qualified_leads / total_leads * 100) if total_leads > 0 else 0,
                    "conversion_rate": conversion_rate,
                    "follow_up_responses": follow_up_responses,
                    "response_rate": response_rate
                },
                "budget_analysis": {
                    "average_budget": round(average_budget, 2),
                    "min_budget": min_budget,
                    "max_budget": max_budget,
                    "currency": "AED"
                },
                "distribution": {
                    "by_source": source_distribution,
                    "by_area": area_distribution,
                    "by_property_type": property_type_distribution,
                    "by_bedrooms": bedroom_distribution,
                    "by_status": status_distribution
                },
                "top_areas": [{"area": area, "count": count} for area, count in top_areas],
                "properties_in_demand": properties_in_demand,
                "quality_metrics": {
                    "average_qualification_score": round(average_score, 2),
                    "verified_percentage": (qualified_leads / total_leads * 100) if total_leads > 0 else 0
                }
            }
            
            logger.info("Metrics calculated successfully")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metrics": {}
            }


class DashboardGeneratorTool(BaseTool):
    name: str = "Dashboard Generator"
    description: str = (
        "Generates comprehensive dashboards and reports from lead data. "
        "Creates HTML, PDF, and JSON format reports with visualizations."
    )
    
    def _run(self, metrics: Dict[str, Any], format: str = "html", 
             output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate dashboard from metrics
        
        Args:
            metrics: Metrics dictionary from MetricsCalculatorTool
            format: Output format (html, pdf, json)
            output_path: Optional custom output path
            
        Returns:
            Result dictionary with dashboard file path
        """
        try:
            logger.info(f"Generating dashboard in {format} format")
            
            if not metrics.get('success'):
                return {
                    "success": False,
                    "error": "Invalid metrics data provided"
                }
            
            # Determine output path
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = "dashboards"
                os.makedirs(output_dir, exist_ok=True)
                output_path = f"{output_dir}/dashboard_{timestamp}.{format}"
            
            # Generate dashboard based on format
            if format == "html":
                dashboard_content = self._generate_html_dashboard(metrics)
            elif format == "json":
                dashboard_content = self._generate_json_dashboard(metrics)
            elif format == "pdf":
                dashboard_content = self._generate_pdf_dashboard(metrics)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported format: {format}"
                }
            
            # Write dashboard to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(dashboard_content)
            
            result = {
                "success": True,
                "format": format,
                "output_path": output_path,
                "file_size": len(dashboard_content),
                "timestamp": datetime.now().isoformat(),
                "metrics_summary": metrics.get('summary', {})
            }
            
            logger.info(f"Dashboard generated successfully: {output_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating dashboard: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_html_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Generate HTML dashboard"""
        summary = metrics.get('summary', {})
        budget = metrics.get('budget_analysis', {})
        top_areas = metrics.get('top_areas', [])
        quality = metrics.get('quality_metrics', {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dubai Real Estate Lead Generation Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s;
        }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-card h3 {{
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .metric-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        .metric-card .label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .section {{
            padding: 30px;
            border-top: 1px solid #eee;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        .area-list {{
            list-style: none;
        }}
        .area-item {{
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .area-item .name {{ font-weight: 600; color: #333; }}
        .area-item .count {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 Dubai Real Estate Dashboard</h1>
            <p>Lead Generation Analytics & Insights</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Total Leads Found</h3>
                <div class="value">{summary.get('total_leads_found', 0)}</div>
                <div class="label">New prospects identified</div>
            </div>
            <div class="metric-card">
                <h3>Leads Qualified</h3>
                <div class="value">{summary.get('leads_qualified', 0)}</div>
                <div class="label">{summary.get('qualification_rate', 0):.1f}% qualification rate</div>
            </div>
            <div class="metric-card">
                <h3>Conversion Rate</h3>
                <div class="value">{summary.get('conversion_rate', 0):.1f}%</div>
                <div class="label">Lead to customer conversion</div>
            </div>
            <div class="metric-card">
                <h3>Response Rate</h3>
                <div class="value">{summary.get('response_rate', 0):.1f}%</div>
                <div class="label">{summary.get('follow_up_responses', 0)} responses received</div>
            </div>
        </div>
        
        <div class="section">
            <h2>💰 Budget Analysis</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Average Budget</h3>
                    <div class="value">AED {budget.get('average_budget', 0):,.0f}</div>
                </div>
                <div class="metric-card">
                    <h3>Budget Range</h3>
                    <div class="value" style="font-size: 1.2em;">
                        AED {budget.get('min_budget', 0):,.0f} - {budget.get('max_budget', 0):,.0f}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📍 Top Areas in Demand</h2>
            <ul class="area-list">
                {''.join(f'<li class="area-item"><span class="name">{area["area"]}</span><span class="count">{area["count"]} leads</span></li>' for area in top_areas[:5])}
            </ul>
        </div>
        
        <div class="section">
            <h2>⭐ Quality Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Avg Qualification Score</h3>
                    <div class="value">{quality.get('average_qualification_score', 0):.1f}</div>
                    <div class="label">Out of 10</div>
                </div>
                <div class="metric-card">
                    <h3>Verified Leads</h3>
                    <div class="value">{quality.get('verified_percentage', 0):.1f}%</div>
                    <div class="label">Contact information verified</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Dubai Real Estate Lead Generation Workflow</p>
            <p>Powered by CrewAI Multi-Agent System</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _generate_json_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Generate JSON dashboard"""
        dashboard_data = {
            "dashboard_type": "Dubai Real Estate Lead Generation",
            "generated_at": datetime.now().isoformat(),
            "metrics": metrics,
            "version": "1.0.0"
        }
        return json.dumps(dashboard_data, indent=2)
    
    def _generate_pdf_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Generate PDF dashboard (returns HTML for now, can be converted to PDF)"""
        # In production, use libraries like reportlab or weasyprint to generate actual PDF
        # For now, return HTML that can be converted to PDF
        return self._generate_html_dashboard(metrics)
