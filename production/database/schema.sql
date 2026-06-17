-- =============================================================================
-- CUSTOMER SUCCESS FTE — CRM/TICKET MANAGEMENT SYSTEM
-- PostgreSQL Schema with pgvector for semantic search
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- =============================================================================
-- TABLE 1: customers
-- Unified customer record across ALL channels
-- =============================================================================
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- =============================================================================
-- TABLE 2: customer_identifiers
-- Links multiple identifiers (email, phone, whatsapp) to one customer
-- Enables cross-channel customer matching
-- =============================================================================
CREATE TABLE customer_identifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    identifier_type VARCHAR(50) NOT NULL,  -- 'email', 'phone', 'whatsapp'
    identifier_value VARCHAR(255) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(identifier_type, identifier_value)
);

-- =============================================================================
-- TABLE 3: conversations
-- One conversation = one support session (may span multiple messages)
-- =============================================================================
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    initial_channel VARCHAR(50) NOT NULL,  -- 'email', 'whatsapp', 'web_form'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'active',   -- 'active', 'resolved', 'escalated', 'pending'
    sentiment_score DECIMAL(3,2),          -- -1.00 to 1.00
    resolution_type VARCHAR(50),           -- 'ai_resolved', 'human_resolved', 'escalated'
    escalated_to VARCHAR(255),             -- Email of human who handled it
    metadata JSONB DEFAULT '{}'
);

-- =============================================================================
-- TABLE 4: messages
-- Every inbound and outbound message with full channel metadata
-- =============================================================================
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    channel VARCHAR(50) NOT NULL,          -- 'email', 'whatsapp', 'web_form'
    direction VARCHAR(20) NOT NULL,        -- 'inbound', 'outbound'
    role VARCHAR(20) NOT NULL,             -- 'customer', 'agent', 'system'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tokens_used INTEGER,
    latency_ms INTEGER,
    tool_calls JSONB DEFAULT '[]',
    channel_message_id VARCHAR(255),       -- Gmail message ID, Twilio SID, form submission ID
    delivery_status VARCHAR(50) DEFAULT 'pending'  -- 'pending', 'sent', 'delivered', 'failed'
);

-- =============================================================================
-- TABLE 5: tickets
-- One ticket = one distinct customer issue
-- =============================================================================
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    customer_id UUID REFERENCES customers(id),
    source_channel VARCHAR(50) NOT NULL,
    category VARCHAR(100),
    priority VARCHAR(20) DEFAULT 'medium',  -- 'low', 'medium', 'high', 'urgent'
    status VARCHAR(50) DEFAULT 'open',      -- 'open', 'processing', 'resolved', 'escalated'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT
);

-- =============================================================================
-- TABLE 6: knowledge_base
-- Product documentation with vector embeddings for semantic search
-- =============================================================================
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    embedding VECTOR(1536),               -- OpenAI text-embedding-ada-002 dimension
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- TABLE 7: channel_configs
-- Per-channel configuration and response templates
-- =============================================================================
CREATE TABLE channel_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel VARCHAR(50) UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    config JSONB NOT NULL DEFAULT '{}',   -- API keys, webhook URLs, etc.
    response_template TEXT,
    max_response_length INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- TABLE 8: agent_metrics
-- Time-series performance data per channel
-- =============================================================================
CREATE TABLE agent_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    channel VARCHAR(50),
    dimensions JSONB DEFAULT '{}',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- INDEXES (Performance critical — do NOT skip)
-- =============================================================================
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customer_identifiers_value ON customer_identifiers(identifier_type, identifier_value);
CREATE INDEX idx_conversations_customer ON conversations(customer_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_channel ON conversations(initial_channel);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_channel ON messages(channel);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
CREATE INDEX idx_tickets_customer ON tickets(customer_id);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_channel ON tickets(source_channel);
CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_agent_metrics_name ON agent_metrics(metric_name, recorded_at DESC);

-- =============================================================================
-- SEED: Default channel configurations
-- =============================================================================
INSERT INTO channel_configs (channel, enabled, config, max_response_length) VALUES
('email', true, '{"max_words": 500, "greeting": "Hi {name},", "closing": "Best regards,\nTechFlow Support"}', 500),
('whatsapp', true, '{"max_chars": 300, "greeting": null, "closing": null, "emoji_allowed": true}', 300),
('web_form', true, '{"max_words": 300, "greeting": "Hello {name},", "closing": "\nTechFlow Support Team"}', 300);
