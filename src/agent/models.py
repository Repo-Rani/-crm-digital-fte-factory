from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any

class Channel(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    WEB_FORM = "web_form"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ResolutionStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class SkillTrigger(str, Enum):
    EVERY_MESSAGE = "every_message"
    PRODUCT_QUESTION = "product_question"
    BEFORE_RESPONSE = "before_response"
    AFTER_GENERATION = "after_generation"
    ON_ESCALATION = "on_escalation"

@dataclass
class CustomerMessage:
    channel: Channel
    customer_id: str
    customer_name: str
    content: str
    email: Optional[str] = None
    subject: Optional[str] = None
    phone: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResponse:
    content: str
    channel: Channel
    should_escalate: bool = False
    escalation_reason: Optional[str] = None
    sentiment_score: float = 0.5
    topics_discussed: List[str] = field(default_factory=list)
    resolution_status: str = "pending"
    response_time_ms: int = 0

@dataclass
class MessageRecord:
    role: str  # "customer" | "agent" | "system"
    content: str
    channel: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sentiment_score: Optional[float] = None
    topics: List[str] = field(default_factory=list)

@dataclass
class ConversationState:
    customer_id: str
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    original_channel: str = ""
    channels_used: List[str] = field(default_factory=list)
    messages: List[MessageRecord] = field(default_factory=list)
    sentiment_trend: List[float] = field(default_factory=list)
    topics_discussed: List[str] = field(default_factory=list)
    resolution_status: ResolutionStatus = ResolutionStatus.OPEN
    escalated_to: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ticket_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SkillDefinition:
    name: str
    description: str
    trigger: SkillTrigger
    inputs: List[str]
    outputs: List[str]
    constraints: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)
