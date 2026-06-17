"""Channel-specific response formatters."""

import re

def format_for_channel(response: str, channel: str, customer_name: str = "Customer") -> str:
    """Format response for the specific channel's style and length limits."""

    if channel == 'email':
        formatted = f"Hi {customer_name},\n\n{response}\n\nBest regards,\nTechFlow Support\n---\nPowered by TechFlow AI. Reply to continue the conversation."
        
        # Enforce 500-word limit (rough estimate by splitting)
        words = formatted.split()
        if len(words) > 500:
            formatted = ' '.join(words[:480]) + '...\n\nBest regards,\nTechFlow Support'
        return formatted

    elif channel == 'whatsapp':
        # Strip markdown formatting for WhatsApp
        clean = response.replace('**', '').replace('__', '').replace('*', '')
        
        # Convert numbered lists to arrow format
        clean = re.sub(r'^\d+\. ', '→ ', clean, flags=re.MULTILINE)
        
        # Enforce 300-char limit for WhatsApp
        if len(clean) > 280:
            clean = clean[:260] + '... Reply "more" for details'
        return clean

    elif channel == 'web_form':
        formatted = f"Hello {customer_name},\n\n{response}\n\nTechFlow Support Team"
        
        # Enforce 300-word limit
        words = formatted.split()
        if len(words) > 300:
            formatted = ' '.join(words[:280]) + '...\n\nTechFlow Support Team'
        return formatted
        
    return response # Fallback
