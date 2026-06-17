from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from .models import ConversationState, MessageRecord, ResolutionStatus

class ConversationMemory:
    def __init__(self):
        self._store: Dict[str, ConversationState] = {}

    def get_or_create(self, customer_id: str, customer_name: str, channel: str, email: Optional[str] = None, phone: Optional[str] = None) -> ConversationState:
        # Cross-channel detection and merging
        if email:
            for state_id, state in self._store.items():
                if state.customer_email == email or state_id == email:
                    # Update existing state with phone if missing
                    if phone and not state.customer_phone:
                        state.customer_phone = phone
                    # If current ID is different (e.g., phone), we should use the existing state
                    if state_id != customer_id:
                        # Simple merge for prototype: update last_updated and channel
                        state.last_updated = datetime.now(timezone.utc).isoformat()
                        if channel not in state.channels_used:
                            state.channels_used.append(channel)
                        
                        # Link this ID to the same state
                        self._store[customer_id] = state
                        return state

        if customer_id in self._store:
            state = self._store[customer_id]
            state.last_updated = datetime.now(timezone.utc).isoformat()
            if channel not in state.channels_used:
                state.channels_used.append(channel)
            return state

        # Create new state
        new_state = ConversationState(
            customer_id=customer_id,
            customer_name=customer_name,
            customer_email=email,
            customer_phone=phone,
            original_channel=channel,
            channels_used=[channel]
        )
        self._store[customer_id] = new_state
        return new_state

    def add_message(self, customer_id: str, role: str, content: str, channel: str, sentiment: Optional[float] = None, topics: List[str] = None) -> None:
        if customer_id not in self._store:
            raise ValueError(f"Customer {customer_id} not found in memory")
        
        state = self._store[customer_id]
        record = MessageRecord(
            role=role,
            content=content,
            channel=channel,
            sentiment_score=sentiment,
            topics=topics or []
        )
        state.messages.append(record)
        state.last_updated = datetime.now(timezone.utc).isoformat()
        
        if topics:
            for topic in topics:
                if topic not in state.topics_discussed:
                    state.topics_discussed.append(topic)

    def update_sentiment_trend(self, customer_id: str, sentiment_score: float) -> None:
        if customer_id in self._store:
            state = self._store[customer_id]
            state.sentiment_trend.append(sentiment_score)
            if len(state.sentiment_trend) > 20:
                state.sentiment_trend.pop(0)

    def is_sentiment_declining(self, customer_id: str) -> bool:
        if customer_id not in self._store:
            return False
        trend = self._store[customer_id].sentiment_trend
        if len(trend) < 3:
            return False
        # Strictly declining: last < second last < third last
        return trend[-1] < trend[-2] < trend[-3]

    def update_resolution_status(self, customer_id: str, status: ResolutionStatus, escalated_to: Optional[str] = None) -> None:
        if customer_id in self._store:
            state = self._store[customer_id]
            state.resolution_status = status
            if escalated_to:
                state.escalated_to = escalated_to
            state.last_updated = datetime.now(timezone.utc).isoformat()

    def get_history_for_agent(self, customer_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
        if customer_id not in self._store:
            return []
        messages = self._store[customer_id].messages[-max_messages:]
        return [
            {
                "role": m.role,
                "content": m.content,
                "channel": m.channel,
                "timestamp": m.timestamp
            } for m in messages
        ]

    def generate_daily_report(self) -> Dict[str, Any]:
        total = len(self._store)
        if total == 0:
            return {"total_conversations": 0}
        
        all_sentiments = []
        escalations = 0
        resolved = 0
        topics = {}
        channels = {"email": {"count": 0, "sentiments": []}, "whatsapp": {"count": 0, "sentiments": []}, "web_form": {"count": 0, "sentiments": []}}

        for state in self._store.values():
            if state.resolution_status == ResolutionStatus.ESCALATED:
                escalations += 1
            if state.resolution_status == ResolutionStatus.RESOLVED:
                resolved += 1
            
            all_sentiments.extend(state.sentiment_trend)
            
            for topic in state.topics_discussed:
                topics[topic] = topics.get(topic, 0) + 1
            
            ch = state.original_channel
            if ch in channels:
                channels[ch]["count"] += 1
                channels[ch]["sentiments"].extend(state.sentiment_trend)

        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.5
        
        report = {
            "total_conversations": total,
            "avg_sentiment_score": round(avg_sentiment, 2),
            "escalation_rate_percent": round((escalations / total) * 100, 2),
            "resolution_rate_percent": round((resolved / total) * 100, 2),
            "most_common_topics": sorted(topics.keys(), key=lambda x: topics[x], reverse=True)[:5],
            "channel_breakdown": {}
        }
        
        for ch, data in channels.items():
            report["channel_breakdown"][ch] = {
                "count": data["count"],
                "avg_sentiment": round(sum(data["sentiments"]) / len(data["sentiments"]), 2) if data["sentiments"] else 0.5
            }
            
        return report
