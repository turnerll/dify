-- 222.place Database Schema
-- Additional tables for social matching functionality

-- Questions table for onboarding
CREATE TABLE IF NOT EXISTS social_questions (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    question_text_en TEXT NOT NULL,
    question_text_es TEXT NOT NULL,
    question_type VARCHAR(20) NOT NULL, -- 'multiple_choice', 'scale', 'text', 'multi_select'
    options JSONB, -- For multiple choice options
    weight DECIMAL(3,2) DEFAULT 1.0, -- Importance weight for matching
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles for extended social information
CREATE TABLE IF NOT EXISTS social_profiles (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    display_name VARCHAR(100),
    bio TEXT,
    location_city VARCHAR(100),
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    max_distance_km INTEGER DEFAULT 50,
    age_range_min INTEGER,
    age_range_max INTEGER,
    preferred_language VARCHAR(10) DEFAULT 'en',
    profile_completed BOOLEAN DEFAULT false,
    privacy_settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- User responses to onboarding questions
CREATE TABLE IF NOT EXISTS social_responses (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES social_questions(id) ON DELETE CASCADE,
    response_value TEXT NOT NULL,
    response_metadata JSONB, -- Additional context or structured data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, question_id)
);

-- Calculated matches between users
CREATE TABLE IF NOT EXISTS social_matches (
    id SERIAL PRIMARY KEY,
    user_id_1 UUID REFERENCES accounts(id) ON DELETE CASCADE,
    user_id_2 UUID REFERENCES accounts(id) ON DELETE CASCADE,
    compatibility_score DECIMAL(5,2) NOT NULL,
    match_reasons JSONB, -- Detailed breakdown of match factors
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'declined', 'blocked'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id_1, user_id_2),
    CONSTRAINT different_users CHECK (user_id_1 != user_id_2),
    CONSTRAINT ordered_user_ids CHECK (user_id_1 < user_id_2)
);

-- Events for social gatherings
CREATE TABLE IF NOT EXISTS social_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) NOT NULL, -- 'dinner', 'gathering', 'outing'
    venue_name VARCHAR(200),
    venue_address TEXT,
    venue_lat DECIMAL(10, 8),
    venue_lng DECIMAL(11, 8),
    event_date TIMESTAMP NOT NULL,
    max_participants INTEGER DEFAULT 10,
    budget_min DECIMAL(8,2),
    budget_max DECIMAL(8,2),
    dietary_accommodations TEXT[],
    accessibility_features TEXT[],
    language_preference VARCHAR(10) DEFAULT 'en',
    created_by UUID REFERENCES accounts(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'open', -- 'open', 'full', 'cancelled', 'completed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event invitations and RSVPs
CREATE TABLE IF NOT EXISTS social_invitations (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES social_events(id) ON DELETE CASCADE,
    inviter_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    invitee_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    invitation_message TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
    response_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, invitee_id)
);

-- Social groups for ongoing connections
CREATE TABLE IF NOT EXISTS social_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    group_type VARCHAR(50) DEFAULT 'casual', -- 'casual', 'activity', 'professional'
    privacy_level VARCHAR(20) DEFAULT 'open', -- 'open', 'invite_only', 'private'
    max_members INTEGER DEFAULT 50,
    created_by UUID REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Group memberships
CREATE TABLE IF NOT EXISTS social_group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES social_groups(id) ON DELETE CASCADE,
    user_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- 'member', 'moderator', 'admin'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, user_id)
);

-- Messages for communication
CREATE TABLE IF NOT EXISTS social_messages (
    id SERIAL PRIMARY KEY,
    conversation_type VARCHAR(20) NOT NULL, -- 'direct', 'group', 'event'
    conversation_id VARCHAR(50) NOT NULL, -- UUID or group_id or event_id
    sender_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text', -- 'text', 'image', 'system'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Moderation flags for content and user reporting
CREATE TABLE IF NOT EXISTS social_moderation_flags (
    id SERIAL PRIMARY KEY,
    reporter_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    reported_user_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    content_type VARCHAR(50), -- 'profile', 'message', 'event', 'user_behavior'
    content_id VARCHAR(100), -- ID of the flagged content
    reason VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'reviewed', 'resolved', 'dismissed'
    moderator_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_social_profiles_user_id ON social_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_social_profiles_location ON social_profiles USING GIST(
    ll_to_earth(location_lat, location_lng)
) WHERE location_lat IS NOT NULL AND location_lng IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_social_responses_user_id ON social_responses(user_id);
CREATE INDEX IF NOT EXISTS idx_social_responses_question_id ON social_responses(question_id);

CREATE INDEX IF NOT EXISTS idx_social_matches_user1 ON social_matches(user_id_1);
CREATE INDEX IF NOT EXISTS idx_social_matches_user2 ON social_matches(user_id_2);
CREATE INDEX IF NOT EXISTS idx_social_matches_score ON social_matches(compatibility_score DESC);

CREATE INDEX IF NOT EXISTS idx_social_events_date ON social_events(event_date);
CREATE INDEX IF NOT EXISTS idx_social_events_type ON social_events(event_type);
CREATE INDEX IF NOT EXISTS idx_social_events_status ON social_events(status);
CREATE INDEX IF NOT EXISTS idx_social_events_creator ON social_events(created_by);

CREATE INDEX IF NOT EXISTS idx_social_invitations_event ON social_invitations(event_id);
CREATE INDEX IF NOT EXISTS idx_social_invitations_invitee ON social_invitations(invitee_id);

CREATE INDEX IF NOT EXISTS idx_social_messages_conversation ON social_messages(conversation_type, conversation_id);
CREATE INDEX IF NOT EXISTS idx_social_messages_sender ON social_messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_social_messages_created ON social_messages(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_social_flags_reporter ON social_moderation_flags(reporter_id);
CREATE INDEX IF NOT EXISTS idx_social_flags_reported ON social_moderation_flags(reported_user_id);
CREATE INDEX IF NOT EXISTS idx_social_flags_status ON social_moderation_flags(status);