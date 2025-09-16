-- 222.place Matchmaking Platform Database Schema
-- PostgreSQL with pgvector extension for similarity matching

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create database
CREATE DATABASE matchmaking_db;
\c matchmaking_db;

-- Users table - Core user accounts
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles - Extended user information
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(20),
    bio TEXT,
    avatar_url VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timezone VARCHAR(50) DEFAULT 'UTC',
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_profile_complete BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Onboarding questions template
CREATE TABLE onboarding_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(50) NOT NULL, -- interests, availability, location, etc.
    question_text_en TEXT NOT NULL,
    question_text_es TEXT NOT NULL,
    question_type VARCHAR(20) NOT NULL, -- multiple_choice, scale, text, etc.
    options JSONB, -- For multiple choice questions
    is_required BOOLEAN DEFAULT true,
    weight DECIMAL(3,2) DEFAULT 1.0, -- Weight for matching algorithm
    display_order INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User responses to onboarding questions
CREATE TABLE onboarding_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES onboarding_questions(id),
    response_value TEXT NOT NULL,
    response_score DECIMAL(5,2), -- Normalized score for matching
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, question_id)
);

-- User matches
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    matched_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    compatibility_score DECIMAL(5,2) NOT NULL,
    similarity_vector vector(384), -- For embedding-based matching
    match_factors JSONB, -- Breakdown of what contributed to the match
    is_mutual BOOLEAN DEFAULT false,
    viewed_at TIMESTAMP,
    liked_at TIMESTAMP,
    passed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, matched_user_id)
);

-- Events - Both suggested and user-created
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) NOT NULL, -- dinner, gathering, outing, etc.
    venue_name VARCHAR(200),
    venue_address TEXT,
    venue_latitude DECIMAL(10, 8),
    venue_longitude DECIMAL(11, 8),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    max_participants INTEGER,
    min_participants INTEGER DEFAULT 2,
    current_participants INTEGER DEFAULT 0,
    tags JSONB, -- Activity tags, interests
    budget_range VARCHAR(20), -- low, medium, high
    is_public BOOLEAN DEFAULT true,
    is_suggested BOOLEAN DEFAULT false, -- AI-suggested vs user-created
    suggestion_algorithm VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active', -- active, cancelled, completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event invitations and RSVPs
CREATE TABLE event_invitations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    inviter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    invitee_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, declined, cancelled
    message TEXT,
    rsvp_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, invitee_id)
);

-- User groups and communities
CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    group_type VARCHAR(30) DEFAULT 'interest', -- interest, location, activity
    is_public BOOLEAN DEFAULT true,
    max_members INTEGER,
    current_members INTEGER DEFAULT 0,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tags JSONB,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Group memberships
CREATE TABLE group_memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- admin, moderator, member
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(group_id, user_id)
);

-- Messages for in-app communication
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text', -- text, image, file
    attachment_url VARCHAR(500),
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_recipient CHECK (
        (recipient_id IS NOT NULL AND group_id IS NULL AND event_id IS NULL) OR
        (recipient_id IS NULL AND group_id IS NOT NULL AND event_id IS NULL) OR
        (recipient_id IS NULL AND group_id IS NULL AND event_id IS NOT NULL)
    )
);

-- Content moderation and abuse reports
CREATE TABLE moderation_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reporter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reported_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content_type VARCHAR(30) NOT NULL, -- message, event, profile, etc.
    content_id UUID NOT NULL,
    reason VARCHAR(50) NOT NULL, -- spam, harassment, inappropriate, etc.
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- pending, reviewed, resolved, dismissed
    moderator_id UUID REFERENCES users(id) ON DELETE SET NULL,
    moderator_notes TEXT,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences and settings
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    distance_preference INTEGER DEFAULT 25, -- km
    age_range_min INTEGER DEFAULT 18,
    age_range_max INTEGER DEFAULT 65,
    notification_email BOOLEAN DEFAULT true,
    notification_push BOOLEAN DEFAULT true,
    privacy_show_distance BOOLEAN DEFAULT true,
    privacy_show_age BOOLEAN DEFAULT true,
    matching_enabled BOOLEAN DEFAULT true,
    embedding_vector vector(384), -- User's preference embedding
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity logs for auditing
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(30),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification queue
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(30) NOT NULL, -- match, message, event_invite, etc.
    title VARCHAR(200) NOT NULL,
    content TEXT,
    data JSONB,
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_location ON profiles(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX idx_onboarding_responses_user_id ON onboarding_responses(user_id);
CREATE INDEX idx_onboarding_responses_question_id ON onboarding_responses(question_id);
CREATE INDEX idx_matches_user_id ON matches(user_id);
CREATE INDEX idx_matches_matched_user_id ON matches(matched_user_id);
CREATE INDEX idx_matches_score ON matches(compatibility_score DESC);
CREATE INDEX idx_matches_created_at ON matches(created_at DESC);
CREATE INDEX idx_events_creator_id ON events(creator_id);
CREATE INDEX idx_events_start_time ON events(start_time);
CREATE INDEX idx_events_location ON events(venue_latitude, venue_longitude) WHERE venue_latitude IS NOT NULL AND venue_longitude IS NOT NULL;
CREATE INDEX idx_events_type_status ON events(event_type, status);
CREATE INDEX idx_event_invitations_event_id ON event_invitations(event_id);
CREATE INDEX idx_event_invitations_invitee_id ON event_invitations(invitee_id);
CREATE INDEX idx_event_invitations_status ON event_invitations(status);
CREATE INDEX idx_groups_created_by ON groups(created_by);
CREATE INDEX idx_group_memberships_group_id ON group_memberships(group_id);
CREATE INDEX idx_group_memberships_user_id ON group_memberships(user_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_group_id ON messages(group_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_moderation_flags_status ON moderation_flags(status);
CREATE INDEX idx_moderation_flags_reported_user_id ON moderation_flags(reported_user_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(user_id, is_read);
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at DESC);

-- Create vector indexes for similarity search
CREATE INDEX idx_matches_similarity_vector ON matches USING ivfflat (similarity_vector vector_cosine_ops);
CREATE INDEX idx_user_preferences_embedding ON user_preferences USING ivfflat (embedding_vector vector_cosine_ops);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_onboarding_responses_updated_at BEFORE UPDATE ON onboarding_responses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_groups_updated_at BEFORE UPDATE ON groups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default onboarding questions
INSERT INTO onboarding_questions (category, question_text_en, question_text_es, question_type, options, display_order, weight) VALUES 
-- Basic Demographics
('demographics', 'What is your age range?', '¿Cuál es tu rango de edad?', 'multiple_choice', '["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]', 1, 0.8),
('demographics', 'What is your relationship status?', '¿Cuál es tu estado civil?', 'multiple_choice', '["Single", "In a relationship", "Married", "Divorced", "Widowed", "It''s complicated"]', 2, 0.7),

-- Interests and Hobbies  
('interests', 'What are your favorite outdoor activities?', '¿Cuáles son tus actividades al aire libre favoritas?', 'multiple_choice', '["Hiking", "Cycling", "Running", "Swimming", "Rock climbing", "Camping", "Gardening", "Sports", "Walking", "None"]', 10, 1.0),
('interests', 'Which indoor activities do you enjoy?', '¿Qué actividades de interior disfrutas?', 'multiple_choice', '["Reading", "Cooking", "Gaming", "Movies", "Art/Crafts", "Music", "Dancing", "Meditation", "Puzzles", "Board games"]', 11, 1.0),
('interests', 'What type of music do you like?', '¿Qué tipo de música te gusta?', 'multiple_choice', '["Pop", "Rock", "Hip-hop", "Electronic", "Classical", "Jazz", "Country", "Latin", "World", "Indie"]', 12, 0.9),
('interests', 'What are your favorite cuisines?', '¿Cuáles son tus cocinas favoritas?', 'multiple_choice', '["Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian", "French", "Thai", "Japanese", "Vegetarian/Vegan"]', 13, 0.8),

-- Lifestyle and Values
('lifestyle', 'How would you describe your lifestyle?', '¿Cómo describirías tu estilo de vida?', 'multiple_choice', '["Very active", "Moderately active", "Balanced", "Relaxed", "Homebody"]', 20, 1.0),
('lifestyle', 'What is your approach to health and fitness?', '¿Cuál es tu enfoque hacia la salud y el fitness?', 'multiple_choice', '["Very health-conscious", "Somewhat health-conscious", "Balanced approach", "Not a priority", "Prefer not to say"]', 21, 0.8),
('lifestyle', 'How important is spirituality/religion in your life?', '¿Qué tan importante es la espiritualidad/religión en tu vida?', 'scale', '{"min": 1, "max": 5, "labels": ["Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]}', 22, 0.7),
('lifestyle', 'What is your relationship with alcohol?', '¿Cuál es tu relación con el alcohol?', 'multiple_choice', '["Don''t drink", "Rarely drink", "Social drinker", "Regular drinker", "Prefer not to say"]', 23, 0.6),

-- Availability and Communication
('availability', 'When are you usually free for activities?', '¿Cuándo sueles estar libre para actividades?', 'multiple_choice', '["Weekday mornings", "Weekday afternoons", "Weekday evenings", "Weekend mornings", "Weekend afternoons", "Weekend evenings", "Flexible schedule"]', 30, 1.0),
('availability', 'How much notice do you prefer for planned activities?', '¿Con cuánta anticipación prefieres planificar actividades?', 'multiple_choice', '["Same day", "1-2 days", "3-7 days", "1-2 weeks", "More than 2 weeks"]', 31, 0.8),
('availability', 'How often would you like to meet new people?', '¿Con qué frecuencia te gustaría conocer gente nueva?', 'multiple_choice', '["Daily", "Few times per week", "Weekly", "Bi-weekly", "Monthly", "Occasionally"]', 32, 0.9),

-- Location and Transportation
('location', 'How far are you willing to travel for activities?', '¿Qué tan lejos estás dispuesto a viajar para actividades?', 'multiple_choice', '["Walking distance (1-2 km)", "Short drive (5-10 km)", "Moderate distance (10-25 km)", "Longer distance (25-50 km)", "Anywhere in the city"]', 40, 1.0),
('location', 'What is your primary mode of transportation?', '¿Cuál es tu principal medio de transporte?', 'multiple_choice', '["Walking", "Bicycle", "Public transit", "Car", "Rideshare", "Motorcycle"]', 41, 0.7),

-- Budget and Spending
('budget', 'What is your typical budget for social activities?', '¿Cuál es tu presupuesto típico para actividades sociales?', 'multiple_choice', '["Free activities only", "Under $20", "$20-50", "$50-100", "$100+", "No specific budget"]', 50, 0.9),
('budget', 'How do you prefer to split costs in group activities?', '¿Cómo prefieres dividir los costos en actividades grupales?', 'multiple_choice', '["Split equally", "Pay for own", "Take turns paying", "Higher earners pay more", "Depends on the situation"]', 51, 0.6),

-- Dietary and Accessibility
('dietary', 'Do you have any dietary restrictions?', '¿Tienes alguna restricción alimentaria?', 'multiple_choice', '["None", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Kosher", "Halal", "Other allergies"]', 60, 0.8),
('accessibility', 'Do you have any accessibility needs we should consider?', '¿Tienes alguna necesidad de accesibilidad que debamos considerar?', 'multiple_choice', '["None", "Wheelchair accessible venues", "Hearing accommodations", "Visual accommodations", "Mobility assistance", "Prefer not to say"]', 61, 0.7),

-- Social Preferences
('social', 'What size groups do you prefer for activities?', '¿Qué tamaño de grupo prefieres para actividades?', 'multiple_choice', '["One-on-one", "Small groups (3-5)", "Medium groups (6-10)", "Large groups (10+)", "No preference"]', 70, 1.0),
('social', 'How do you prefer to communicate initially?', '¿Cómo prefieres comunicarte inicialmente?', 'multiple_choice', '["In-app messaging", "Phone calls", "Video calls", "Meet in public place", "Through mutual friends"]', 71, 0.8),
('social', 'What is your comfort level with meeting strangers?', '¿Cuál es tu nivel de comodidad al conocer extraños?', 'scale', '{"min": 1, "max": 5, "labels": ["Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Somewhat comfortable", "Very comfortable"]}', 72, 0.9),

-- Personality and Values
('personality', 'How would you describe your energy level?', '¿Cómo describirías tu nivel de energía?', 'scale', '{"min": 1, "max": 5, "labels": ["Very low energy", "Low energy", "Moderate", "High energy", "Very high energy"]}', 80, 0.8),
('personality', 'Are you more of an introvert or extrovert?', '¿Eres más introvertido o extrovertido?', 'scale', '{"min": 1, "max": 5, "labels": ["Very introverted", "Somewhat introverted", "Balanced", "Somewhat extroverted", "Very extroverted"]}', 81, 0.9),
('personality', 'How important is punctuality to you?', '¿Qué tan importante es la puntualidad para ti?', 'scale', '{"min": 1, "max": 5, "labels": ["Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]}', 82, 0.7),

-- Cultural and Language
('cultural', 'What languages do you speak?', '¿Qué idiomas hablas?', 'multiple_choice', '["English only", "Spanish only", "English and Spanish", "English and other", "Spanish and other", "Multiple languages"]', 90, 0.8),
('cultural', 'How important is cultural diversity in your social circle?', '¿Qué tan importante es la diversidad cultural en tu círculo social?', 'scale', '{"min": 1, "max": 5, "labels": ["Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]}', 91, 0.7),

-- Goals and Expectations
('goals', 'What are you hoping to get from this platform?', '¿Qué esperas obtener de esta plataforma?', 'multiple_choice', '["Make new friends", "Find activity partners", "Professional networking", "Romantic connections", "Community involvement", "Learn new skills"]', 100, 1.0),
('goals', 'How long do you typically like to get to know someone before meeting?', '¿Cuánto tiempo te gusta conocer a alguien antes de encontrarte?', 'multiple_choice', '["Immediately", "A few messages", "A few days", "A week or more", "Depends on the person"]', 101, 0.8);

-- Create admin user (password: admin123)
INSERT INTO users (id, email, password_hash, is_active, is_verified) 
VALUES (
    'admin-user-uuid-here-12345678',
    'admin@222place.local',
    crypt('admin123', gen_salt('bf')),
    true,
    true
);

INSERT INTO profiles (user_id, first_name, last_name, display_name, city, country, preferred_language, is_profile_complete)
VALUES (
    'admin-user-uuid-here-12345678',
    'Admin',
    'User',
    'Admin',
    'Local City',
    'Local Country',
    'en',
    true
);