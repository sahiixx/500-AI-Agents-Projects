"""
Communication tools for WhatsApp, Email, and n8n webhook integration
"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from crewai_tools import BaseTool
import json

logger = logging.getLogger(__name__)


class TwilioWhatsAppTool(BaseTool):
    name: str = "Twilio WhatsApp Integration"
    description: str = (
        "Sends WhatsApp messages to qualified leads using Twilio API. "
        "Supports personalized message templates."
    )
    
    def _run(self, leads: List[Dict[str, Any]], message_template: str) -> Dict[str, Any]:
        """
        Send WhatsApp messages to leads
        
        Args:
            leads: List of lead dictionaries
            message_template: Message template with placeholders
            
        Returns:
            Result dictionary with success status
        """
        try:
            # In production, use Twilio client
            # from twilio.rest import Client
            
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
            
            logger.info(f"Sending WhatsApp messages to {len(leads)} leads")
            
            sent_count = 0
            failed_count = 0
            
            for lead in leads:
                try:
                    # Format message with lead data
                    message = message_template.format(
                        name=lead.get('name', 'there'),
                        area=lead.get('preferred_area', 'Dubai'),
                        property_type=lead.get('property_type', 'property'),
                        bedrooms=lead.get('bedrooms', '1-2'),
                        price=f"{lead.get('budget', 0):,}",
                        property_location=lead.get('preferred_area', 'Dubai')
                    )
                    
                    # Mock: In production, send via Twilio
                    # client = Client(account_sid, auth_token)
                    # message = client.messages.create(
                    #     from_=whatsapp_number,
                    #     body=message,
                    #     to=f"whatsapp:{lead['phone']}"
                    # )
                    
                    sent_count += 1
                    logger.debug(f"WhatsApp sent to {lead.get('name')}")
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send WhatsApp to {lead.get('name')}: {str(e)}")
            
            result = {
                "success": True,
                "sent_count": sent_count,
                "failed_count": failed_count,
                "total_leads": len(leads),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"WhatsApp messages sent: {sent_count}/{len(leads)}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp messages: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "sent_count": 0,
                "failed_count": len(leads)
            }


class EmailTool(BaseTool):
    name: str = "Email Integration"
    description: str = (
        "Sends personalized emails to qualified leads. "
        "Supports HTML templates and attachments."
    )
    
    def _run(self, leads: List[Dict[str, Any]], email_template: str, 
             subject: str = "Your Perfect Dubai Property Match") -> Dict[str, Any]:
        """
        Send emails to leads
        
        Args:
            leads: List of lead dictionaries
            email_template: Email template with placeholders
            subject: Email subject line
            
        Returns:
            Result dictionary with success status
        """
        try:
            # In production, use SMTP or email service
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")
            from_email = os.getenv("FROM_EMAIL")
            
            logger.info(f"Sending emails to {len(leads)} leads")
            
            sent_count = 0
            failed_count = 0
            
            for lead in leads:
                try:
                    # Format email with lead data
                    email_body = email_template.format(
                        name=lead.get('name', 'there'),
                        area=lead.get('preferred_area', 'Dubai'),
                        property_type=lead.get('property_type', 'property'),
                        bedrooms=lead.get('bedrooms', '1-2'),
                        price=f"{lead.get('budget', 0):,}",
                        property_location=lead.get('preferred_area', 'Dubai')
                    )
                    
                    # Mock: In production, send via SMTP
                    # msg = MIMEMultipart()
                    # msg['From'] = from_email
                    # msg['To'] = lead['email']
                    # msg['Subject'] = subject
                    # msg.attach(MIMEText(email_body, 'plain'))
                    
                    # server = smtplib.SMTP(smtp_host, smtp_port)
                    # server.starttls()
                    # server.login(smtp_username, smtp_password)
                    # server.send_message(msg)
                    # server.quit()
                    
                    sent_count += 1
                    logger.debug(f"Email sent to {lead.get('name')}")
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send email to {lead.get('name')}: {str(e)}")
            
            result = {
                "success": True,
                "sent_count": sent_count,
                "failed_count": failed_count,
                "total_leads": len(leads),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Emails sent: {sent_count}/{len(leads)}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending emails: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "sent_count": 0,
                "failed_count": len(leads)
            }


class N8NWebhookTool(BaseTool):
    name: str = "n8n Webhook Integration"
    description: str = (
        "Sends lead data to n8n workflow via webhook. "
        "Enables advanced automation and integration with other services."
    )
    
    def _run(self, leads: List[Dict[str, Any]], event_type: str = "new_leads") -> Dict[str, Any]:
        """
        Send lead data to n8n webhook
        
        Args:
            leads: List of lead dictionaries
            event_type: Type of event to trigger
            
        Returns:
            Result dictionary with success status
        """
        try:
            import requests
            
            webhook_url = os.getenv("N8N_WEBHOOK_URL")
            api_key = os.getenv("N8N_API_KEY")
            
            if not webhook_url:
                logger.warning("N8N_WEBHOOK_URL not configured")
                return {
                    "success": False,
                    "error": "Webhook URL not configured"
                }
            
            logger.info(f"Sending {len(leads)} leads to n8n webhook")
            
            # Prepare payload
            payload = {
                "event_type": event_type,
                "timestamp": datetime.now().isoformat(),
                "lead_count": len(leads),
                "leads": leads
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            # Send to webhook
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = {
                "success": True,
                "status_code": response.status_code,
                "lead_count": len(leads),
                "response": response.json() if response.text else {},
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully sent leads to n8n webhook")
            return result
            
        except Exception as e:
            logger.error(f"Error sending to n8n webhook: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "lead_count": len(leads)
            }
