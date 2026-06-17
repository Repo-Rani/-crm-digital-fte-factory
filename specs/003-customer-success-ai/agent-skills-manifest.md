# Agent Skills Manifest

## knowledge_retrieval
**Description:** Search product documentation for authoritative answers

**Trigger:** product_question

**Inputs:** customer_query

**Outputs:** relevant_docs, confidence_score

**Constraints:**
- Only return documented info
- Escalate after 2 failures

---

## sentiment_analysis
**Description:** Evaluate customer emotional state from message text

**Trigger:** every_message

**Inputs:** message_text

**Outputs:** sentiment_score, sentiment_label

**Constraints:**
- Score < 0.3 triggers escalation
- Detect CAPS lock

---

## escalation_decision
**Description:** Determine if human intervention is required

**Trigger:** after_generation

**Inputs:** message_content, sentiment_score

**Outputs:** should_escalate, reason

**Constraints:**
- 8 hard triggers
- Strict adherence

---

## channel_adaptation
**Description:** Format response for specific channel constraints

**Trigger:** before_response

**Inputs:** response_text, channel

**Outputs:** formatted_response

**Constraints:**
- WhatsApp max 300c
- Email greeting required

---

## customer_identification
**Description:** Unify customer identity across multiple channels

**Trigger:** every_message

**Inputs:** metadata

**Outputs:** customer_id, unified_history

**Constraints:**
- Email is primary key
- Merge phone and email

---

