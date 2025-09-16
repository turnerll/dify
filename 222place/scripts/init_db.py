#!/usr/bin/env python3
"""
Initialize 222.place database schema and seed data
"""
import os
import sys
import logging
from pathlib import Path

# Add API directory to path
api_dir = Path(__file__).parent.parent / 'api'
sys.path.insert(0, str(api_dir))

from flask import Flask
from extensions.ext_database import db
from configs import dify_config
from app_factory import create_app
from seed_data import get_questions, get_sample_users, get_sample_events
import uuid
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the 222.place database tables"""
    logger.info("Initializing 222.place database schema...")
    
    # Read and execute schema file
    schema_file = Path(__file__).parent / 'schema.sql'
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    try:
        # Execute schema creation
        db.session.execute(schema_sql)
        db.session.commit()
        logger.info("Database schema created successfully")
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        db.session.rollback()
        raise

def seed_questions():
    """Seed onboarding questions"""
    logger.info("Seeding onboarding questions...")
    
    questions = get_questions()
    
    for question in questions:
        try:
            # Check if question already exists
            existing = db.session.execute(
                "SELECT id FROM social_questions WHERE question_text_en = :text",
                {'text': question['question_text_en']}
            ).fetchone()
            
            if existing:
                logger.debug(f"Question already exists: {question['question_text_en'][:50]}...")
                continue
            
            # Insert new question
            insert_sql = """
                INSERT INTO social_questions (
                    category, question_text_en, question_text_es, question_type, 
                    options, weight, is_required
                ) VALUES (
                    :category, :text_en, :text_es, :type, :options, :weight, :required
                )
            """
            
            db.session.execute(insert_sql, {
                'category': question['category'],
                'text_en': question['question_text_en'],
                'text_es': question['question_text_es'],
                'type': question['question_type'],
                'options': json.dumps(question.get('options')),
                'weight': question.get('weight', 1.0),
                'required': question.get('is_required', True)
            })
            
        except Exception as e:
            logger.error(f"Error inserting question: {e}")
            db.session.rollback()
            raise
    
    db.session.commit()
    logger.info(f"Seeded {len(questions)} questions")

def seed_users():
    """Seed sample users"""
    logger.info("Seeding sample users...")
    
    users = get_sample_users()
    
    for user_data in users:
        try:
            # Check if user already exists
            existing = db.session.execute(
                "SELECT id FROM accounts WHERE email = :email",
                {'email': user_data['email']}
            ).fetchone()
            
            if existing:
                logger.debug(f"User already exists: {user_data['email']}")
                continue
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            # Insert into accounts table (simplified - you may need to adjust based on actual schema)
            insert_user_sql = """
                INSERT INTO accounts (
                    id, name, email, password_hash, interface_language, 
                    status, created_at, updated_at
                ) VALUES (
                    :id, :name, :email, :password_hash, :language, 
                    'active', :created_at, :updated_at
                )
            """
            
            now = datetime.utcnow()
            
            db.session.execute(insert_user_sql, {
                'id': user_id,
                'name': user_data['name'],
                'email': user_data['email'],
                'password_hash': '$2b$12$demo.hash.for.testing.purposes.only',  # Demo hash
                'language': user_data.get('preferred_language', 'en'),
                'created_at': now,
                'updated_at': now
            })
            
            # Insert into social_profiles table
            insert_profile_sql = """
                INSERT INTO social_profiles (
                    user_id, display_name, bio, location_city, location_lat, location_lng,
                    preferred_language, profile_completed, created_at, updated_at
                ) VALUES (
                    :user_id, :display_name, :bio, :city, :lat, :lng,
                    :language, true, :created_at, :updated_at
                )
            """
            
            db.session.execute(insert_profile_sql, {
                'user_id': user_id,
                'display_name': user_data['display_name'],
                'bio': user_data['bio'],
                'city': user_data['location_city'],
                'lat': user_data['location_lat'],
                'lng': user_data['location_lng'],
                'language': user_data.get('preferred_language', 'en'),
                'created_at': now,
                'updated_at': now
            })
            
            logger.info(f"Created user: {user_data['email']}")
            
        except Exception as e:
            logger.error(f"Error creating user {user_data['email']}: {e}")
            db.session.rollback()
            raise
    
    db.session.commit()
    logger.info(f"Seeded {len(users)} users")

def seed_events():
    """Seed sample events"""
    logger.info("Seeding sample events...")
    
    events = get_sample_events()
    
    # Get a user to be the event creator
    creator = db.session.execute("SELECT id FROM accounts LIMIT 1").fetchone()
    if not creator:
        logger.warning("No users found, skipping event seeding")
        return
    
    creator_id = creator.id
    
    for event_data in events:
        try:
            # Check if event already exists
            existing = db.session.execute(
                "SELECT id FROM social_events WHERE title = :title",
                {'title': event_data['title']}
            ).fetchone()
            
            if existing:
                logger.debug(f"Event already exists: {event_data['title']}")
                continue
            
            # Insert event
            insert_event_sql = """
                INSERT INTO social_events (
                    title, description, event_type, venue_name, venue_address,
                    venue_lat, venue_lng, event_date, max_participants,
                    budget_min, budget_max, dietary_accommodations,
                    language_preference, created_by, created_at, updated_at
                ) VALUES (
                    :title, :description, :type, :venue_name, :venue_address,
                    :lat, :lng, :event_date, :max_participants,
                    :budget_min, :budget_max, :dietary_accommodations,
                    :language, :created_by, :created_at, :updated_at
                )
            """
            
            # Set event date to be in the near future
            event_date = datetime.utcnow() + timedelta(days=7)
            now = datetime.utcnow()
            
            db.session.execute(insert_event_sql, {
                'title': event_data['title'],
                'description': event_data['description'],
                'type': event_data['event_type'],
                'venue_name': event_data['venue_name'],
                'venue_address': event_data['venue_address'],
                'lat': event_data['venue_lat'],
                'lng': event_data['venue_lng'],
                'event_date': event_date,
                'max_participants': event_data['max_participants'],
                'budget_min': event_data['budget_min'],
                'budget_max': event_data['budget_max'],
                'dietary_accommodations': event_data.get('dietary_accommodations', []),
                'language': event_data.get('language_preference', 'en'),
                'created_by': creator_id,
                'created_at': now,
                'updated_at': now
            })
            
            logger.info(f"Created event: {event_data['title']}")
            
        except Exception as e:
            logger.error(f"Error creating event {event_data['title']}: {e}")
            db.session.rollback()
            raise
    
    db.session.commit()
    logger.info(f"Seeded {len(events)} events")

def seed_sample_responses():
    """Seed sample responses for testing matching"""
    logger.info("Seeding sample responses...")
    
    # Get all users and questions
    users = db.session.execute("SELECT id FROM accounts").fetchall()
    questions = db.session.execute("SELECT id, category FROM social_questions").fetchall()
    
    if not users or not questions:
        logger.warning("No users or questions found, skipping response seeding")
        return
    
    # Create some sample responses for the first few users
    sample_responses = {
        'demographics': ['26-35', '36-45', '25'],
        'interests': ['Cooking,Reading,Music', 'Sports,Travel,Technology', 'Art,Dancing,Movies'],
        'dining': ['Italian,Mexican,Asian', 'Vegetarian', 'Casual restaurants,Fine dining'],
        'social': ['Small groups (3-5)', 'Somewhat outgoing', 'Deep philosophical discussions,Humor and jokes'],
        'availability': ['Friday,Saturday,Sunday', 'Early evening,Late evening', 'Weekly'],
        'budget': ['$40-60', '$50-100', 'Split evenly'],
        'accessibility': ['Car', 'None', 'Yes, I drink'],
        'culture': ['All cultures', 'Honesty,Kindness,Humor', 'Not very important'],
        'activities': ['Dinner parties,Game nights,Cultural events', 'Concerts,Theater shows,Food festivals', 'Love trying new things'],
        'communication': ['Text messages,App notifications', 'Somewhat open'],
        'lifestyle': ['Balanced', 'No pets', 'Live alone', 'Established career']
    }
    
    for i, user in enumerate(users[:3]):  # Only seed for first 3 users
        user_id = user.id
        
        for question in questions:
            question_id = question.id
            category = question.category
            
            if category in sample_responses:
                responses_for_category = sample_responses[category]
                response_value = responses_for_category[i % len(responses_for_category)]
                
                try:
                    insert_response_sql = """
                        INSERT INTO social_responses (user_id, question_id, response_value)
                        VALUES (:user_id, :question_id, :response_value)
                        ON CONFLICT (user_id, question_id) DO NOTHING
                    """
                    
                    db.session.execute(insert_response_sql, {
                        'user_id': user_id,
                        'question_id': question_id,
                        'response_value': response_value
                    })
                    
                except Exception as e:
                    logger.error(f"Error inserting response: {e}")
                    continue
    
    db.session.commit()
    logger.info("Seeded sample responses")

def main():
    """Main function to initialize and seed the database"""
    try:
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            logger.info("Starting 222.place database initialization...")
            
            # Initialize schema
            init_database()
            
            # Seed data
            seed_questions()
            seed_users()
            seed_events()
            seed_sample_responses()
            
            logger.info("222.place database initialization completed successfully!")
            
            # Print summary
            question_count = db.session.execute("SELECT COUNT(*) FROM social_questions").scalar()
            user_count = db.session.execute("SELECT COUNT(*) FROM social_profiles").scalar()
            event_count = db.session.execute("SELECT COUNT(*) FROM social_events").scalar()
            
            print(f"\n=== 222.place Database Summary ===")
            print(f"Questions: {question_count}")
            print(f"Users: {user_count}")
            print(f"Events: {event_count}")
            print(f"Database ready for testing!")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()