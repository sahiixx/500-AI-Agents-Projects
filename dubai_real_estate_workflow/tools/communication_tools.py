"""
Communication tools for sending messages via WhatsApp, Email, and n8n webhooks
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from crewai_tools import BaseTool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

logger = logging.getLogger(__name__)


class TwilioWhatsAppTool(BaseTool):
    name: str = "Twilio WhatsApp Messenger"
    description: str = (
        "Sends WhatsApp messages to leads using Twilio API. "
        "Supports personalized messages with property details."
    )
    
    def _run(self, leads: List[Dict[str, Any]], template: Optional[str] = None) -> Dict[str, Any]:
        """
        Send WhatsApp messages to leads via Twilio
        
        Args:
            leads: List of lead dictionaries with contact information
            template: Optional custom message template
            
        Returns:
            Result dictionary with success status and details
        """
        try:
            # In production, use Twilio SDK
            # from twilio.rest import Client
            
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
            
            logger.info(f"Sending WhatsApp messages to {len(leads)} leads")
            
            # Mock implementation
            # In production:
            # client = Client(account_sid, auth_token)
            
            sent_count = 0
            failed_count = 0
            message_ids = []
            
            # Default template if none provided
            if not template:
                template = """Hi {name}! 👋

Found a perfect match for you in {area}:
🏠 {property_type} | {bedrooms} BHK
💰 AED {price}
📍 {property_location}

Interested in a viewing? Reply YES to schedule!"""
            
            for lead in leads:
                try:
                    # Format message with lead data
                    message_body = template.format(
                        name=lead.get('name', 'there'),
                        area=lead.get('preferred_area', 'Dubai'),
                        property_type=lead.get('property_type', 'apartment'),
                        bedrooms=lead.get('bedrooms', '1'),
                        price=f"{lead.get('budget', 800000):,}",
                        property_location=lead.get('preferred_area', 'Dubai')
                    )
                    
                    to_number = lead.get('phone', '')
                    if not to_number.startswith('whatsapp:'):
                        to_number = f"whatsapp:{to_number}"
                    
                    # Mock: In production, send via Twilio
                    # message = client.messages.create(
                    #     body=message_body,
                    #     from_=whatsapp_number,
                    #     to=to_number
                    # )
                    # message_ids.append(message.sid)
                    
                    mock_message_id = f"SM{sent_count:010d}"
                    message_ids.append(mock_message_id)
                    sent_count += 1
                    
                    logger.debug(f"WhatsApp sent to {lead.get('name')}: {mock_message_id}")
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send WhatsApp to {lead.get('name')}: {str(e)}")
            
            result = {
                "success": True,
                "channel": "WhatsApp",
                "sent_count": sent_count,
                "failed_count": failed_count,
                "total_leads": len(leads),
                "message_ids": message_ids,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully sent {sent_count} WhatsApp messages via Twilio")
            return result
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp messages: {str(e)}")
            return {
                "success": False,
                "channel": "WhatsApp",
                "error": str(e),
                "sent_count": 0,
                "failed_count": len(leads)
            }


class EmailTool(BaseTool):
    name: str = "Email Sender"
    description: str = (
        "Sends personalized emails to leads with property information. "
        "Supports HTML formatting and attachments."
    )
    
    def _run(self, leads: List[Dict[str, Any]], subject: Optional[str] = None, 
             template: Optional[str] = None) -> Dict[str, Any]:
        """
        Send emails to leads
        
        Args:
            leads: List of lead dictionaries with contact information
            subject: Email subject line
            template: Optional custom email template
            
        Returns:
            Result dictionary with success status and details
        """
        try:
            smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")
            from_email = os.getenv("FROM_EMAIL", smtp_username)
            
            logger.info(f"Sending emails to {len(leads)} leads")
            
            # Default subject and template
            if not subject:
                subject = "Exclusive Dubai Property Match - Perfect for You!"
            
            if not template:
                template = """Hello {name},

I hope this message finds you well. I noticed your interest in Dubai real estate, 
particularly in the {area} area.

I have an excellent property match for you:
- Location: {property_location}
- Type: {property_type}
- Bedrooms: {bedrooms}
- Price: AED {price}
- Status: {property_status}

This property offers exceptional value and matches your stated preferences perfectly.

Would you be interested in scheduling a viewing or learning more about this opportunity?

Best regards,
Dubai Real Estate Team

---
This is an automated message. Reply to this email to connect with our team.
"""
            
            sent_count = 0
            failed_count = 0
            
            # Mock SMTP connection
            # In production:
            # server = smtplib.SMTP(smtp_host, smtp_port)
            # server.starttls()
            # server.login(smtp_username, smtp_password)
            
            for lead in leads:
                try:
                    # Create message
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = subject
                    msg['From'] = from_email
                    msg['To'] = lead.get('email', '')
                    
                    # Format email body
                    email_body = template.format(
                        name=lead.get('name', 'Valued Client'),
                        area=lead.get('preferred_area', 'Dubai'),
                        property_location=lead.get('preferred_area', 'Dubai'),
                        property_type=lead.get('property_type', 'apartment'),
                        bedrooms=lead.get('bedrooms', '1'),
                        price=f"{lead.get('budget', 800000):,}",
                        property_status=lead.get('property_status', 'ready')
                    )
                    
                    # Attach plain text
                    text_part = MIMEText(email_body, 'plain')
                    msg.attach(text_part)
                    
                    # Mock: In production, send via SMTP
                    # server.send_message(msg)
                    
                    sent_count += 1
                    logger.debug(f"Email sent to {lead.get('name')} at {lead.get('email')}")
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send email to {lead.get('name')}: {str(e)}")
            
            # Mock: In production, close connection
            # server.quit()
            
            result = {
                "success": True,
                "channel": "Email",
                "sent_count": sent_count,
                "failed_count": failed_count,
                "total_leads": len(leads),
                "subject": subject,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully sent {sent_count} emails")
            return result
            
        except Exception as e:
            logger.error(f"Error sending emails: {str(e)}")
            return {
                "success": False,
                "channel": "Email",
                "error": str(e),
                "sent_count": 0,
                "failed_count": len(leads)
            }


class N8NWebhookTool(BaseTool):
    name: str = "n8n Webhook Integration"
    description: str = (
        "Sends lead data to n8n workflow automation via webhook. "
        "Triggers automated workflows for lead processing and notifications."
    )
    
    def _run(self, leads: List[Dict[str, Any]], workflow_type: str = "lead_notification") -> Dict[str, Any]:
        """
        Send lead data to n8n webhook
        
        Args:
            leads: List of lead dictionaries
            workflow_type: Type of n8n workflow to trigger
            
        Returns:
            Result dictionary with success status and details
        """
        try:
            webhook_url = os.getenv("N8N_WEBHOOK_URL")
            api_key = os.getenv("N8N_API_KEY", "")
            
            if not webhook_url:
                logger.warning("N8N_WEBHOOK_URL not configured")
                return {
                    "success": False,
                    "error": "N8N_WEBHOOK_URL not configured",
                    "sent_count": 0
                }
            
            logger.info(f"Sending {len(leads)} leads to n8n webhook")
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            sent_count = 0
            failed_count = 0
            webhook_responses = []
            
            for lead in leads:
                try:
                    # Prepare webhook payload
                    payload = {
                        "workflow_type": workflow_type,
                        "timestamp": datetime.now().isoformat(),
                        "lead": {
                            "name": lead.get('name'),
                            "email": lead.get('email'),
                            "phone": lead.get('phone'),
                            "budget": lead.get('budget'),
                            "preferred_area": lead.get('preferred_area'),
                            "property_type": lead.get('property_type'),
                            "bedrooms": lead.get('bedrooms'),
                            "source": lead.get('source'),
                            "status": lead.get('status', 'new'),
                            "verified": lead.get('verified', False),
                            "qualification_score": lead.get('qualification_score', 0)
                        }
                    }
                    
                    # Mock: In production, send to n8n
                    # response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
                    # response.raise_for_status()
                    # webhook_responses.append(response.json())
                    
                    mock_response = {
                        "status": "success",
                        "workflow_id": f"wf_{sent_count:06d}",
                        "execution_id": f"exec_{sent_count:08d}"
                    }
                    webhook_responses.append(mock_response)
                    
                    sent_count += 1
                    logger.debug(f"Webhook triggered for {lead.get('name')}")
                    
                except requests.exceptions.RequestException as e:
                    failed_count += 1
                    logger.error(f"Failed to send webhook for {lead.get('name')}: {str(e)}")
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Unexpected error for {lead.get('name')}: {str(e)}")
            
            result = {
                "success": True,
                "channel": "n8n Webhook",
                "sent_count": sent_count,
                "failed_count": failed_count,
                "total_leads": len(leads),
                "workflow_type": workflow_type,
                "webhook_url": webhook_url,
                "responses": webhook_responses,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully triggered {sent_count} n8n webhooks")
            return result
            
        except Exception as e:
            logger.error(f"Error sending n8n webhooks: {str(e)}")
            return {
                "success": False,
                "channel": "n8n Webhook",
                "error": str(e),
                "sent_count": 0,
                "failed_count": len(leads)
            }
