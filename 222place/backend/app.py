#!/usr/bin/env python3
"""
Simple Flask API server for 222.place social matching
"""
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import json
from datetime import datetime, timedelta
import bcrypt
from geopy.distance import geodesic
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '222place-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', '222place-jwt-secret')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://postgres:222place123@localhost:5432/place222')
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://:222place123@localhost:6379/0')
    
    # Enable CORS
    CORS(app, origins=['http://localhost', 'http://localhost:80', 'http://localhost:3000'])
    
    # JWT Manager
    jwt = JWTManager(app)
    
    # Database connection
    def get_db():
        return psycopg2.connect(app.config['DATABASE_URL'], cursor_factory=RealDictCursor)
    
    # Redis connection
    def get_redis():
        redis_url = app.config['REDIS_URL']
        return redis.from_url(redis_url)
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        try:
            # Test database connection
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT 1')
            
            # Test Redis connection
            r = get_redis()
            r.ping()
            
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'database': 'connected',
                'redis': 'connected'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/v1/social/onboarding/questions')
    def get_questions():
        """Get onboarding questions"""
        try:
            lang = request.args.get('lang', 'en')
            
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, category, question_text_en, question_text_es, 
                               question_type, options, weight, is_required
                        FROM social_questions 
                        ORDER BY category, id
                    """)
                    
                    questions = []
                    for row in cur.fetchall():
                        question_text = row['question_text_es'] if lang == 'es' else row['question_text_en']
                        questions.append({
                            'id': row['id'],
                            'category': row['category'],
                            'question_text': question_text,
                            'question_type': row['question_type'],
                            'options': row['options'],
                            'weight': float(row['weight']) if row['weight'] else 1.0,
                            'is_required': row['is_required']
                        })
            
            return jsonify({
                'questions': questions,
                'total_count': len(questions),
                'language': lang
            })
            
        except Exception as e:
            logger.error(f"Error fetching questions: {e}")
            return jsonify({'error': 'Failed to fetch questions'}), 500
    
    @app.route('/v1/social/onboarding/responses', methods=['POST'])
    def submit_responses():
        """Submit onboarding responses"""
        try:
            data = request.get_json()
            if not data or 'responses' not in data:
                return jsonify({'error': 'Responses are required'}), 400
            
            responses = data['responses']
            user_id = data.get('user_id', '00000000-0000-0000-0000-000000000001')  # Demo user
            
            with get_db() as conn:
                with conn.cursor() as cur:
                    # Insert responses
                    for response in responses:
                        cur.execute("""
                            INSERT INTO social_responses (user_id, question_id, response_value, response_metadata)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (user_id, question_id) 
                            DO UPDATE SET 
                                response_value = EXCLUDED.response_value,
                                response_metadata = EXCLUDED.response_metadata,
                                updated_at = CURRENT_TIMESTAMP
                        """, (
                            user_id,
                            response['question_id'],
                            str(response['response_value']),
                            json.dumps(response.get('metadata', {}))
                        ))
                    
                    # Update or create profile
                    profile_data = data.get('profile', {})
                    if profile_data:
                        cur.execute("""
                            INSERT INTO social_profiles (
                                user_id, display_name, bio, location_city, location_lat, location_lng,
                                max_distance_km, preferred_language, profile_completed
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (user_id) DO UPDATE SET
                                display_name = COALESCE(EXCLUDED.display_name, social_profiles.display_name),
                                bio = COALESCE(EXCLUDED.bio, social_profiles.bio),
                                location_city = COALESCE(EXCLUDED.location_city, social_profiles.location_city),
                                location_lat = COALESCE(EXCLUDED.location_lat, social_profiles.location_lat),
                                location_lng = COALESCE(EXCLUDED.location_lng, social_profiles.location_lng),
                                preferred_language = COALESCE(EXCLUDED.preferred_language, social_profiles.preferred_language),
                                profile_completed = true,
                                updated_at = CURRENT_TIMESTAMP
                        """, (
                            user_id,
                            profile_data.get('display_name'),
                            profile_data.get('bio'),
                            profile_data.get('location_city'),
                            profile_data.get('location_lat'),
                            profile_data.get('location_lng'),
                            profile_data.get('max_distance_km', 50),
                            profile_data.get('preferred_language', 'en'),
                            True
                        ))
                
                conn.commit()
            
            return jsonify({
                'message': 'Responses saved successfully',
                'responses_count': len(responses)
            })
            
        except Exception as e:
            logger.error(f"Error saving responses: {e}")
            return jsonify({'error': 'Failed to save responses'}), 500
    
    @app.route('/v1/social/matching', methods=['POST'])
    def generate_matches():
        """Generate matches for a user"""
        try:
            user_id = request.json.get('user_id', '00000000-0000-0000-0000-000000000001')
            
            # Simple matching logic (demo)
            matches = [
                {
                    'user_id': '00000000-0000-0000-0000-000000000002',
                    'compatibility_score': 0.85,
                    'match_reasons': ['Similar interests', 'Close location', 'Compatible schedule']
                },
                {
                    'user_id': '00000000-0000-0000-0000-000000000003',
                    'compatibility_score': 0.72,
                    'match_reasons': ['Food preferences match', 'Same language preference']
                }
            ]
            
            return jsonify({
                'message': 'Matches generated successfully',
                'matches_count': len(matches),
                'matches': matches
            })
            
        except Exception as e:
            logger.error(f"Error generating matches: {e}")
            return jsonify({'error': 'Failed to generate matches'}), 500
    
    @app.route('/v1/social/matching')
    def get_matches():
        """Get existing matches for a user"""
        try:
            user_id = request.args.get('user_id', '00000000-0000-0000-0000-000000000001')
            limit = min(int(request.args.get('limit', 20)), 50)
            
            # Demo matches
            matches = [
                {
                    'id': 1,
                    'matched_user': {
                        'id': '00000000-0000-0000-0000-000000000002',
                        'display_name': 'Maria',
                        'bio': 'Love exploring new restaurants and cultural events',
                        'location_city': 'San Francisco'
                    },
                    'compatibility_score': 0.85,
                    'match_reasons': ['Similar interests', 'Close location'],
                    'status': 'pending'
                },
                {
                    'id': 2,
                    'matched_user': {
                        'id': '00000000-0000-0000-0000-000000000003',
                        'display_name': 'Alex',
                        'bio': 'Photographer who loves concerts and outdoor activities',
                        'location_city': 'Berkeley'
                    },
                    'compatibility_score': 0.72,
                    'match_reasons': ['Food preferences match', 'Same language'],
                    'status': 'pending'
                }
            ]
            
            return jsonify({
                'matches': matches[:limit],
                'has_more': len(matches) > limit
            })
            
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
            return jsonify({'error': 'Failed to fetch matches'}), 500
    
    @app.route('/v1/social/events')
    def get_events():
        """Get available events"""
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, title, description, event_type, venue_name, venue_address,
                               event_date, max_participants, budget_min, budget_max,
                               language_preference, status
                        FROM social_events 
                        WHERE status = 'open' AND event_date > NOW()
                        ORDER BY event_date ASC
                        LIMIT 20
                    """)
                    
                    events = []
                    for row in cur.fetchall():
                        events.append({
                            'id': row['id'],
                            'title': row['title'],
                            'description': row['description'],
                            'event_type': row['event_type'],
                            'venue_name': row['venue_name'],
                            'venue_address': row['venue_address'],
                            'event_date': row['event_date'].isoformat() if row['event_date'] else None,
                            'max_participants': row['max_participants'],
                            'budget_range': f"${row['budget_min']}-${row['budget_max']}" if row['budget_min'] and row['budget_max'] else None,
                            'language_preference': row['language_preference'],
                            'status': row['status']
                        })
            
            return jsonify({
                'events': events,
                'total_count': len(events)
            })
            
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return jsonify({'error': 'Failed to fetch events'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)