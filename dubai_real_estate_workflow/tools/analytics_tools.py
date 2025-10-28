"""
Analytics and reporting tools for lead generation metrics
"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from crewai_tools import BaseTool
import json

logger = logging.getLogger(__name__)


class MetricsCalculatorTool(BaseTool):
    name: str = "Metrics Calculator"
    description: str = (
        "Calculates key metrics for lead generation performance. "
        "Provides insights on conversion rates, lead quality, and trends."
    )
    
    def _run(self, all_leads: List[Dict[str, Any]], 
             qualified_leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate lead generation metrics
        
        Args:
            all_leads: All leads found
            qualified_leads: Qualified leads only
            
        Returns:
            Dictionary with calculated metrics
        """
        try:
            logger.info("Calculating lead generation metrics")
            
            metrics = {
                "total_leads": len(all_leads),
                "qualified_leads": len(qualified_leads),
                "qualification_rate": 0,
                "average_budget": 0,
                "top_areas": {},
                "top_sources": {},
                "property_type_distribution": {},
                "verification_rate": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            # Calculate qualification rate
            if all_leads:
                metrics["qualification_rate"] = (len(qualified_leads) / len(all_leads)) * 100
            
            # Calculate average budget
            if qualified_leads:
                budgets = [lead.get('budget', 0) for lead in qualified_leads if lead.get('budget')]
                if budgets:
                    metrics["average_budget"] = sum(budgets) / len(budgets)
                    metrics["min_budget"] = min(budgets)
                    metrics["max_budget"] = max(budgets)
            
            # Top areas
            areas = {}
            for lead in qualified_leads:
                area = lead.get('preferred_area', 'Unknown')
                areas[area] = areas.get(area, 0) + 1
            metrics["top_areas"] = dict(sorted(areas.items(), key=lambda x: x[1], reverse=True)[:5])
            
            # Top sources
            sources = {}
            for lead in all_leads:
                source = lead.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            metrics["top_sources"] = sources
            
            # Property type distribution
            property_types = {}
            for lead in qualified_leads:
                prop_type = lead.get('property_type', 'Unknown')
                property_types[prop_type] = property_types.get(prop_type, 0) + 1
            metrics["property_type_distribution"] = property_types
            
            # Verification rate
            verified_count = sum(1 for lead in all_leads if lead.get('verified', False))
            if all_leads:
                metrics["verification_rate"] = (verified_count / len(all_leads)) * 100
            
            logger.info(f"Metrics calculated successfully")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


class DashboardGeneratorTool(BaseTool):
    name: str = "Dashboard Generator"
    description: str = (
        "Generates HTML dashboard with visualizations and insights. "
        "Creates comprehensive reports for lead generation performance."
    )
    
    def _run(self, metrics: Dict[str, Any], output_file: str = "dashboard.html") -> Dict[str, Any]:
        """
        Generate HTML dashboard
        
        Args:
            metrics: Metrics dictionary from MetricsCalculatorTool
            output_file: Output file path
            
        Returns:
            Result dictionary with file path
        """
        try:
            logger.info("Generating dashboard")
            
            # Create HTML dashboard
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dubai Real Estate Lead Generation Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-card h3 {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .metric-card .value {{
            color: #667eea;
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .metric-card .subvalue {{
            color: #999;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .chart-section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .chart-section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        
        .bar-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .bar-label {{
            min-width: 150px;
            font-weight: 500;
        }}
        
        .bar-container {{
            flex: 1;
            background: #f0f0f0;
            border-radius: 5px;
            height: 30px;
            position: relative;
            overflow: hidden;
        }}
        
        .bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            transition: width 1s ease;
        }}
        
        .footer {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            color: #666;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .status-success {{
            background: #10b981;
            color: white;
        }}
        
        .status-warning {{
            background: #f59e0b;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 Dubai Real Estate Lead Generation</h1>
            <p>Performance Dashboard & Analytics</p>
            <span class="status-badge status-success">✓ Active</span>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Total Leads Found</h3>
                <div class="value">{metrics.get('total_leads', 0)}</div>
                <div class="subvalue">From all sources</div>
            </div>
            
            <div class="metric-card">
                <h3>Qualified Leads</h3>
                <div class="value">{metrics.get('qualified_leads', 0)}</div>
                <div class="subvalue">{metrics.get('qualification_rate', 0):.1f}% qualification rate</div>
            </div>
            
            <div class="metric-card">
                <h3>Average Budget</h3>
                <div class="value">AED {metrics.get('average_budget', 0):,.0f}</div>
                <div class="subvalue">Per qualified lead</div>
            </div>
            
            <div class="metric-card">
                <h3>Verification Rate</h3>
                <div class="value">{metrics.get('verification_rate', 0):.1f}%</div>
                <div class="subvalue">Contact verified</div>
            </div>
        </div>
        
        <div class="chart-section">
            <h2>📊 Top Preferred Areas</h2>
            <div class="bar-chart">
"""
            
            # Add top areas chart
            top_areas = metrics.get('top_areas', {})
            max_area_count = max(top_areas.values()) if top_areas else 1
            
            for area, count in top_areas.items():
                percentage = (count / max_area_count) * 100
                html_content += f"""
                <div class="bar-item">
                    <div class="bar-label">{area}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {percentage}%">{count}</div>
                    </div>
                </div>
"""
            
            html_content += """
            </div>
        </div>
        
        <div class="chart-section">
            <h2>📱 Leads by Source</h2>
            <div class="bar-chart">
"""
            
            # Add sources chart
            top_sources = metrics.get('top_sources', {})
            max_source_count = max(top_sources.values()) if top_sources else 1
            
            for source, count in top_sources.items():
                percentage = (count / max_source_count) * 100
                html_content += f"""
                <div class="bar-item">
                    <div class="bar-label">{source}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {percentage}%">{count}</div>
                    </div>
                </div>
"""
            
            html_content += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            <p style="margin-top: 10px; color: #999;">Dubai Real Estate Lead Generation System v1.0</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Write to file
            output_path = os.path.join(os.path.dirname(__file__), '..', output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            result = {
                "success": True,
                "output_file": output_path,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Dashboard generated: {output_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating dashboard: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
