import os
import json
import time
from typing import List, Dict, Optional, Any, Tuple
from src.agent.models import CustomerMessage, AgentResponse, Channel, ResolutionStatus
from src.agent.memory import ConversationMemory

class CustomerSuccessAgent:
    def __init__(self, 
                 knowledge_base_path: str = "context/product-docs.md",
                 brand_voice_path: str = "context/brand-voice.md",
                 escalation_rules_path: str = "context/escalation-rules.md"):
        
        self.knowledge_base_path = knowledge_base_path
        self.brand_voice_path = brand_voice_path
        self.escalation_rules_path = escalation_rules_path
        
        self.knowledge_base = self._load_file(knowledge_base_path)
        self.brand_voice = self._load_file(brand_voice_path)
        self.escalation_rules = self._load_file(escalation_rules_path)
        
        self.memory = ConversationMemory()
        
        # Simple keywords for topic extraction
        self.topic_keywords = {
            "password": "password_reset",
            "reset": "password_reset",
            "billing": "billing",
            "invoice": "billing",
            "charge": "billing",
            "refund": "refund",
            "slack": "integration",
            "github": "integration",
            "zapier": "integration",
            "api": "api",
            "webhook": "api",
            "task": "task_management",
            "project": "project_management",
            "sso": "technical",
            "login": "technical",
            "security": "security"
        }

    def _load_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def normalize_message(self, raw_message: Dict[str, Any]) -> CustomerMessage:
        channel_str = raw_message.get("channel", "email")
        channel = Channel(channel_str)
        
        customer_name = raw_message.get("customer_name", "Customer")
        timestamp = raw_message.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        content = ""
        customer_id = ""
        email = raw_message.get("customer_email")
        subject = raw_message.get("subject")
        phone = raw_message.get("customer_phone")
        
        if channel == Channel.EMAIL:
            content = raw_message.get("content", "")
            customer_id = raw_message.get("customer_email", "unknown@example.com")
            email = customer_id
        elif channel == Channel.WHATSAPP:
            content = raw_message.get("content", "")
            customer_id = phone or "unknown_phone"
        elif channel == Channel.WEB_FORM:
            content = raw_message.get("message", raw_message.get("content", ""))
            customer_id = raw_message.get("customer_email", "unknown@webform.com")
            email = customer_id
            
        return CustomerMessage(
            channel=channel,
            customer_id=customer_id,
            customer_name=customer_name,
            content=content,
            email=email,
            subject=subject,
            phone=phone,
            timestamp=timestamp,
            metadata=raw_message
        )

    def analyze_sentiment(self, text: str) -> float:
        score = 0.5  # Default neutral
        if not text:
            return score
            
        text_lower = text.lower()
        
        # Positive words
        pos_words = ["thank", "great", "love", "amazing", "helpful", "excellent"]
        for word in pos_words:
            if word in text_lower:
                score += 0.2
                
        # Negative words
        neg_words = ["broken", "terrible", "useless", "awful", "disappointed"]
        for word in neg_words:
            if word in text_lower:
                score -= 0.2
                
        # Angry words
        angry_words = ["angry", "furious", "hate", "unacceptable", "disgusting"]
        for word in angry_words:
            if word in text_lower:
                score -= 0.3
                
        # CAPS LOCK detection
        words = text.split()
        if len(words) > 3:
            caps_count = sum(1 for w in words if w.isupper() and len(w) > 1)
            if caps_count / len(words) > 0.3:
                score -= 0.3
                
        # Profanity (simple check)
        profanity = ["fuck", "shit", "asshole"]
        for p in profanity:
            if p in text_lower:
                score -= 0.5
                
        # Overrides
        legal_words = ["lawyer", "sue", "attorney", "legal"]
        if any(w in text_lower for w in legal_words):
            return 0.0
            
        return max(-1.0, min(1.0, score))

    def check_escalation_needed(self, message: CustomerMessage, sentiment: float) -> Tuple[bool, Optional[str]]:
        content_lower = message.content.lower().strip()
        subject_lower = (message.subject or "").lower().strip()
        combined_text = f" {subject_lower} {content_lower} ".strip()
        
        import re
        def has_word(text, word_list):
            for word in word_list:
                pattern = rf"\b{re.escape(word)}\b"
                if re.search(pattern, text, re.IGNORECASE):
                    return True
            return False

        if not combined_text:
            return True, "empty_message"
            
        # 1. Refund & Money (Hard Trigger)
        if has_word(combined_text, ["refund", "money back", "chargeback", "reverse charge"]):
            return True, "refund_request"
            
        # 2. Pricing & Plans (Hard Trigger for negotiation/inquiry)
        if has_word(combined_text, ["discount", "negotiate", "pricing", "trial", "how much", "cost", "plan", "subscription"]):
            return True, "pricing_inquiry"
            
        # 3. Legal & Compliance (Hard Trigger)
        if has_word(combined_text, ["lawyer", "attorney", "sue", "legal", "court", "gdpr", "compliance", "dispute", "litigation"]):
            return True, "legal_threat"
            
        # 4. Explicit Human Request
        if has_word(combined_text, ["human", "agent", "representative", "person", "someone", "call me"]):
            return True, "human_requested"
            
        # 5. Billing (Hard Trigger)
        if has_word(combined_text, ["billing", "invoice", "charged", "bill", "payment"]):
            return True, "billing_question"
            
        # 6. Profanity & Abuse
        if has_word(combined_text, ["fuck", "shit", "asshole", "garbage", "useless", "joke"]):
            return True, "profanity_detected"
            
        # 7. Security Concerns
        if has_word(combined_text, ["leak", "leaked", "hacked", "security", "breach", "unauthorized access", "data breach"]):
            return True, "security_concern"
            
        # 8. Severe Bug / Urgency
        if has_word(combined_text, ["emergency", "disappeared", "down", "critical"]):
            return True, "urgent_issue"
        
        if "urgent" in combined_text and sentiment < 0.6:
            return True, "urgent_issue"

        # 9. Sentiment based
        if sentiment < 0.3:
            return True, "negative_sentiment"
            
        return False, None

    def search_knowledge_base(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        if not self.knowledge_base:
            return []
            
        sections = self.knowledge_base.split("##")
        results = []
        query_words = set(query.lower().split())
        
        if not query_words:
            return []
            
        for section in sections:
            lines = section.strip().split("\n")
            if not lines: continue
            
            title = lines[0].strip()
            content = "\n".join(lines[1:]).strip()
            
            content_lower = content.lower()
            matches = sum(1 for word in query_words if word in content_lower)
            relevance = matches / len(query_words)
            
            if relevance >= 0.1:
                results.append({
                    "title": title,
                    "content": content[:500],
                    "relevance": relevance
                })
                
        return sorted(results, key=lambda x: x["relevance"], reverse=True)[:max_results]

    def generate_response(self, message: CustomerMessage, kb_results: List[Dict[str, Any]], history: List[Dict[str, Any]]) -> str:
        if not kb_results:
            return "I don't have specific information on this, let me connect you with our team."
            
        # Basic RAG-like generation for prototype
        best_result = kb_results[0]
        answer = f"Based on our documentation for {best_result['title']}:\n\n{best_result['content']}"
        
        # Check history for repeats
        if any(best_result['title'].lower() in h['content'].lower() for h in history if h['role'] == 'agent'):
            answer = "As I mentioned earlier, " + answer
            
        return answer

    def format_for_channel(self, response: str, channel: Channel, customer_name: str) -> str:
        if channel == Channel.EMAIL:
            formatted = f"Hi {customer_name},\n\n{response}\n\nBest regards,\nTechFlow Support"
            return formatted
        elif channel == Channel.WHATSAPP:
            # Strip markdown and limit length
            clean = response.replace("**", "").replace("__", "")
            if len(clean) > 250:
                clean = clean[:247] + "..."
            return clean
        elif channel == Channel.WEB_FORM:
            return f"Hello {customer_name},\n\n{response}\n\nTechFlow Support Team"
            
        return response

    def process_message(self, raw_message: Dict[str, Any]) -> AgentResponse:
        start_time = time.time()
        
        try:
            # 1. Normalize
            message = self.normalize_message(raw_message)
            
            # 2. Sentiment
            sentiment = self.analyze_sentiment(message.content)
            
            # 3. Extract topics
            topics = [v for k, v in self.topic_keywords.items() if k in message.content.lower()]
            
            # 4. Check Escalation
            should_escalate, reason = self.check_escalation_needed(message, sentiment)
            
            # Get history
            history = self.memory.get_history_for_agent(message.customer_id)
            
            if should_escalate:
                # Update memory with escalation
                self.memory.get_or_create(message.customer_id, message.customer_name, message.channel, email=message.email, phone=message.phone)
                self.memory.add_message(message.customer_id, "customer", message.content, message.channel, sentiment, topics)
                
                esc_msg = "I've flagged your case for our specialist team. They will reach out soon."
                formatted_esc = self.format_for_channel(esc_msg, message.channel, message.customer_name)
                
                self.memory.add_message(message.customer_id, "agent", formatted_esc, message.channel)
                self.memory.update_resolution_status(message.customer_id, ResolutionStatus.ESCALATED)
                
                return AgentResponse(
                    content=formatted_esc,
                    channel=message.channel,
                    should_escalate=True,
                    escalation_reason=reason,
                    sentiment_score=sentiment,
                    topics_discussed=topics,
                    resolution_status="escalated",
                    response_time_ms=int((time.time() - start_time) * 1000)
                )
            
            # 5. Search KB
            kb_results = self.search_knowledge_base(message.content)
            
            # 6. Generate
            response_text = self.generate_response(message, kb_results, history)
            
            # 7. Format
            formatted_response = self.format_for_channel(response_text, message.channel, message.customer_name)
            
            # 8. Update Memory
            self.memory.get_or_create(message.customer_id, message.customer_name, message.channel, email=message.email, phone=message.phone)
            self.memory.add_message(message.customer_id, "customer", message.content, message.channel, sentiment, topics)
            self.memory.add_message(message.customer_id, "agent", formatted_response, message.channel)
            self.memory.update_sentiment_trend(message.customer_id, sentiment)
            
            status = "pending" if not kb_results else "resolved"
            self.memory.update_resolution_status(message.customer_id, ResolutionStatus.RESOLVED if kb_results else ResolutionStatus.PENDING)

            return AgentResponse(
                content=formatted_response,
                channel=message.channel,
                sentiment_score=sentiment,
                topics_discussed=topics,
                resolution_status=status,
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            
        except Exception as e:
            return AgentResponse(
                content="I'm sorry, I encountered an error processing your request.",
                channel=Channel.EMAIL,
                should_escalate=True,
                escalation_reason="processing_error",
                resolution_status="error"
            )

if __name__ == "__main__":
    agent = CustomerSuccessAgent()
    # Test cases
    test_msg = {
        "channel": "email",
        "customer_email": "test@test.com",
        "customer_name": "Test User",
        "content": "How do I reset my password?",
        "subject": "Help"
    }
    print(agent.process_message(test_msg))
