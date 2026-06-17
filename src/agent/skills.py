import json
import os
from typing import List
from src.agent.models import SkillDefinition, SkillTrigger

def get_skills() -> List[SkillDefinition]:
    return [
        SkillDefinition(
            name="knowledge_retrieval",
            description="Search product documentation for authoritative answers",
            trigger=SkillTrigger.PRODUCT_QUESTION,
            inputs=["customer_query"],
            outputs=["relevant_docs", "confidence_score"],
            constraints=["Only return documented info", "Escalate after 2 failures"],
            examples=[
                {"input": "how to reset password", "output": "link to reset page"},
                {"input": "unknown feature", "output": "escalate"}
            ]
        ),
        SkillDefinition(
            name="sentiment_analysis",
            description="Evaluate customer emotional state from message text",
            trigger=SkillTrigger.EVERY_MESSAGE,
            inputs=["message_text"],
            outputs=["sentiment_score", "sentiment_label"],
            constraints=["Score < 0.3 triggers escalation", "Detect CAPS lock"],
            examples=[
                {"input": "I LOVE THIS", "output": 0.9},
                {"input": "I HATE THIS", "output": 0.1}
            ]
        ),
        SkillDefinition(
            name="escalation_decision",
            description="Determine if human intervention is required",
            trigger=SkillTrigger.AFTER_GENERATION,
            inputs=["message_content", "sentiment_score"],
            outputs=["should_escalate", "reason"],
            constraints=["8 hard triggers", "Strict adherence"],
            examples=[
                {"input": "refund please", "output": "True, refund_request"},
                {"input": "thank you", "output": "False"}
            ]
        ),
        SkillDefinition(
            name="channel_adaptation",
            description="Format response for specific channel constraints",
            trigger=SkillTrigger.BEFORE_RESPONSE,
            inputs=["response_text", "channel"],
            outputs=["formatted_response"],
            constraints=["WhatsApp max 300c", "Email greeting required"],
            examples=[
                {"input": "Hi", "channel": "email", "output": "Hi [Name]..."},
                {"input": "Hi", "channel": "whatsapp", "output": "Hi"}
            ]
        ),
        SkillDefinition(
            name="customer_identification",
            description="Unify customer identity across multiple channels",
            trigger=SkillTrigger.EVERY_MESSAGE,
            inputs=["metadata"],
            outputs=["customer_id", "unified_history"],
            constraints=["Email is primary key", "Merge phone and email"],
            examples=[
                {"input": "phone + email", "output": "merged_state"},
                {"input": "new email", "output": "new_state"}
            ]
        )
    ]

def export_manifest():
    skills = get_skills()
    manifest_path = "specs/003-customer-success-ai/agent-skills-manifest.md"
    
    # Create dir if not exists
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("# Agent Skills Manifest\n\n")
        for s in skills:
            f.write(f"## {s.name}\n")
            f.write(f"**Description:** {s.description}\n\n")
            f.write(f"**Trigger:** {s.trigger.value}\n\n")
            f.write(f"**Inputs:** {', '.join(s.inputs)}\n\n")
            f.write(f"**Outputs:** {', '.join(s.outputs)}\n\n")
            f.write("**Constraints:**\n")
            for c in s.constraints:
                f.write(f"- {c}\n")
            f.write("\n---\n\n")
    
    print(json.dumps([s.__dict__ for s in skills], indent=2, default=lambda x: x.value if isinstance(x, SkillTrigger) else x))

if __name__ == "__main__":
    export_manifest()
