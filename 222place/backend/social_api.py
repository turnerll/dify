"""
222.place API endpoints for social matching
"""
from flask import Blueprint, request, jsonify, current_app
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized
from sqlalchemy import text, and_, or_, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import logging
import uuid
import json
import math

from extensions.ext_database import db
from libs.login import login_required, current_user
from services.errors.account import AccountNotFoundError
from controllers.web import api

logger = logging.getLogger(__name__)

# Create blueprint for 222place endpoints
social_bp = Blueprint('social', __name__, url_prefix='/v1/social')

class OnboardingQuestionsApi(Resource):
    """Get onboarding questions for user registration"""
    
    @login_required
    def get(self):
        """Get all onboarding questions"""
        try:
            # Get preferred language from query params or user profile
            lang = request.args.get('lang', 'en')
            if lang not in ['en', 'es']:
                lang = 'en'
            
            # Query questions from database
            query = text("""
                SELECT id, category, question_text_en, question_text_es, 
                       question_type, options, weight, is_required
                FROM social_questions 
                ORDER BY category, id
            """)
            
            result = db.session.execute(query)
            questions = []
            
            for row in result:
                question_text = row.question_text_es if lang == 'es' else row.question_text_en
                questions.append({
                    'id': row.id,
                    'category': row.category,
                    'question_text': question_text,
                    'question_type': row.question_type,
                    'options': row.options,
                    'weight': float(row.weight) if row.weight else 1.0,
                    'is_required': row.is_required
                })
            
            return {
                'questions': questions,
                'total_count': len(questions),
                'language': lang
            }
            
        except Exception as e:
            logger.error(f"Error fetching onboarding questions: {e}")
            return {'error': 'Failed to fetch questions'}, 500

class OnboardingResponsesApi(Resource):
    """Submit user responses to onboarding questions"""
    
    @login_required 
    def post(self):
        """Submit onboarding responses"""
        try:
            data = request.get_json()
            if not data or 'responses' not in data:
                raise BadRequest('Responses are required')
            
            responses = data['responses']
            user_id = current_user.id
            
            # Validate responses format
            for response in responses:
                if 'question_id' not in response or 'response_value' not in response:
                    raise BadRequest('Each response must have question_id and response_value')
            
            # Insert responses (use ON CONFLICT to handle updates)
            for response in responses:
                query = text("""
                    INSERT INTO social_responses (user_id, question_id, response_value, response_metadata)
                    VALUES (:user_id, :question_id, :response_value, :metadata)
                    ON CONFLICT (user_id, question_id) 
                    DO UPDATE SET 
                        response_value = EXCLUDED.response_value,
                        response_metadata = EXCLUDED.response_metadata,
                        updated_at = CURRENT_TIMESTAMP
                """)
                
                db.session.execute(query, {
                    'user_id': user_id,
                    'question_id': response['question_id'],
                    'response_value': str(response['response_value']),
                    'metadata': json.dumps(response.get('metadata', {}))
                })
            
            # Update or create user profile
            profile_data = data.get('profile', {})
            self._update_user_profile(user_id, profile_data)
            
            db.session.commit()
            
            return {
                'message': 'Responses saved successfully',
                'responses_count': len(responses)
            }
            
        except BadRequest as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving onboarding responses: {e}")
            return {'error': 'Failed to save responses'}, 500
    
    def _update_user_profile(self, user_id, profile_data):
        """Update or create user social profile"""
        query = text("""
            INSERT INTO social_profiles (
                user_id, display_name, bio, location_city, location_lat, location_lng,
                max_distance_km, age_range_min, age_range_max, preferred_language, profile_completed
            ) VALUES (
                :user_id, :display_name, :bio, :location_city, :location_lat, :location_lng,
                :max_distance_km, :age_range_min, :age_range_max, :preferred_language, true
            )
            ON CONFLICT (user_id) DO UPDATE SET
                display_name = COALESCE(EXCLUDED.display_name, social_profiles.display_name),
                bio = COALESCE(EXCLUDED.bio, social_profiles.bio),
                location_city = COALESCE(EXCLUDED.location_city, social_profiles.location_city),
                location_lat = COALESCE(EXCLUDED.location_lat, social_profiles.location_lat),
                location_lng = COALESCE(EXCLUDED.location_lng, social_profiles.location_lng),
                max_distance_km = COALESCE(EXCLUDED.max_distance_km, social_profiles.max_distance_km),
                age_range_min = COALESCE(EXCLUDED.age_range_min, social_profiles.age_range_min),
                age_range_max = COALESCE(EXCLUDED.age_range_max, social_profiles.age_range_max),
                preferred_language = COALESCE(EXCLUDED.preferred_language, social_profiles.preferred_language),
                profile_completed = true,
                updated_at = CURRENT_TIMESTAMP
        """)
        
        db.session.execute(query, {
            'user_id': user_id,
            'display_name': profile_data.get('display_name'),
            'bio': profile_data.get('bio'),
            'location_city': profile_data.get('location_city'),
            'location_lat': profile_data.get('location_lat'),
            'location_lng': profile_data.get('location_lng'),
            'max_distance_km': profile_data.get('max_distance_km', 50),
            'age_range_min': profile_data.get('age_range_min'),
            'age_range_max': profile_data.get('age_range_max'),
            'preferred_language': profile_data.get('preferred_language', 'en')
        })

class MatchingApi(Resource):
    """Generate and retrieve user matches"""
    
    @login_required
    def post(self):
        """Generate new matches for current user"""
        try:
            user_id = current_user.id
            
            # Check if user has completed onboarding
            profile_query = text("SELECT profile_completed FROM social_profiles WHERE user_id = :user_id")
            profile = db.session.execute(profile_query, {'user_id': user_id}).fetchone()
            
            if not profile or not profile.profile_completed:
                return {'error': 'Please complete your profile first'}, 400
            
            # Generate matches using matching algorithm
            matches = self._calculate_matches(user_id)
            
            # Store matches in database
            for match in matches:
                self._save_match(user_id, match)
            
            db.session.commit()
            
            return {
                'message': 'Matches generated successfully',
                'matches_count': len(matches),
                'matches': matches[:10]  # Return top 10 matches
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error generating matches: {e}")
            return {'error': 'Failed to generate matches'}, 500
    
    @login_required 
    def get(self):
        """Get existing matches for current user"""
        try:
            user_id = current_user.id
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            query = text("""
                SELECT 
                    sm.id, sm.compatibility_score, sm.match_reasons, sm.status,
                    CASE 
                        WHEN sm.user_id_1 = :user_id THEN sm.user_id_2 
                        ELSE sm.user_id_1 
                    END as matched_user_id,
                    sp.display_name, sp.bio, sp.location_city,
                    a.name as full_name
                FROM social_matches sm
                JOIN social_profiles sp ON (
                    CASE 
                        WHEN sm.user_id_1 = :user_id THEN sp.user_id = sm.user_id_2 
                        ELSE sp.user_id = sm.user_id_1 
                    END
                )
                JOIN accounts a ON a.id = sp.user_id
                WHERE (sm.user_id_1 = :user_id OR sm.user_id_2 = :user_id)
                AND sm.status != 'blocked'
                ORDER BY sm.compatibility_score DESC, sm.created_at DESC
                LIMIT :limit OFFSET :offset
            """)
            
            result = db.session.execute(query, {
                'user_id': user_id,
                'limit': limit,
                'offset': offset
            })
            
            matches = []
            for row in result:
                matches.append({
                    'id': row.id,
                    'matched_user': {
                        'id': str(row.matched_user_id),
                        'display_name': row.display_name,
                        'full_name': row.full_name,
                        'bio': row.bio,
                        'location_city': row.location_city
                    },
                    'compatibility_score': float(row.compatibility_score),
                    'match_reasons': row.match_reasons,
                    'status': row.status
                })
            
            return {
                'matches': matches,
                'has_more': len(matches) == limit
            }
            
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
            return {'error': 'Failed to fetch matches'}, 500
    
    def _calculate_matches(self, user_id):
        """Calculate compatibility scores with other users"""
        # Get current user's responses
        user_responses = self._get_user_responses(user_id)
        user_profile = self._get_user_profile(user_id)
        
        if not user_responses or not user_profile:
            return []
        
        # Get all other users with completed profiles
        other_users_query = text("""
            SELECT DISTINCT sp.user_id 
            FROM social_profiles sp
            WHERE sp.user_id != :user_id 
            AND sp.profile_completed = true
        """)
        
        other_users = db.session.execute(other_users_query, {'user_id': user_id}).fetchall()
        matches = []
        
        for other_user in other_users:
            other_user_id = other_user.user_id
            other_responses = self._get_user_responses(other_user_id)
            other_profile = self._get_user_profile(other_user_id)
            
            if not other_responses or not other_profile:
                continue
            
            # Calculate compatibility score
            score, reasons = self._calculate_compatibility(
                user_responses, user_profile,
                other_responses, other_profile
            )
            
            if score > 0.3:  # Minimum threshold
                matches.append({
                    'user_id': other_user_id,
                    'compatibility_score': score,
                    'match_reasons': reasons
                })
        
        # Sort by score and apply fairness filter
        matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return self._apply_fairness_filter(matches[:50])  # Top 50 for fairness filtering
    
    def _get_user_responses(self, user_id):
        """Get user responses keyed by question ID"""
        query = text("""
            SELECT sr.question_id, sr.response_value, sq.category, sq.weight
            FROM social_responses sr
            JOIN social_questions sq ON sr.question_id = sq.id
            WHERE sr.user_id = :user_id
        """)
        
        result = db.session.execute(query, {'user_id': user_id})
        responses = {}
        
        for row in result:
            responses[row.question_id] = {
                'value': row.response_value,
                'category': row.category,
                'weight': float(row.weight) if row.weight else 1.0
            }
        
        return responses
    
    def _get_user_profile(self, user_id):
        """Get user profile information"""
        query = text("""
            SELECT * FROM social_profiles WHERE user_id = :user_id
        """)
        
        result = db.session.execute(query, {'user_id': user_id}).fetchone()
        if not result:
            return None
        
        return {
            'location_lat': result.location_lat,
            'location_lng': result.location_lng,
            'max_distance_km': result.max_distance_km or 50,
            'age_range_min': result.age_range_min,
            'age_range_max': result.age_range_max,
            'preferred_language': result.preferred_language or 'en'
        }
    
    def _calculate_compatibility(self, responses1, profile1, responses2, profile2):
        """Calculate compatibility score between two users"""
        total_score = 0
        total_weight = 0
        reasons = []
        
        # Location compatibility
        if (profile1.get('location_lat') and profile1.get('location_lng') and 
            profile2.get('location_lat') and profile2.get('location_lng')):
            
            distance = self._calculate_distance(
                profile1['location_lat'], profile1['location_lng'],
                profile2['location_lat'], profile2['location_lng']
            )
            
            max_distance = min(profile1.get('max_distance_km', 50), profile2.get('max_distance_km', 50))
            
            if distance <= max_distance:
                location_score = max(0, 1 - (distance / max_distance))
                total_score += location_score * 1.0  # High weight for location
                total_weight += 1.0
                reasons.append(f"Within {distance:.1f}km distance")
        
        # Language compatibility
        if profile1.get('preferred_language') == profile2.get('preferred_language'):
            total_score += 1.0 * 0.7
            total_weight += 0.7
            reasons.append("Same preferred language")
        
        # Response compatibility
        common_questions = set(responses1.keys()) & set(responses2.keys())
        
        for question_id in common_questions:
            r1 = responses1[question_id]
            r2 = responses2[question_id]
            
            similarity = self._calculate_response_similarity(r1['value'], r2['value'])
            weight = r1['weight']
            
            total_score += similarity * weight
            total_weight += weight
            
            if similarity > 0.7:
                reasons.append(f"Similar {r1['category']} preferences")
        
        # Calculate final score
        if total_weight == 0:
            return 0, []
        
        final_score = min(total_score / total_weight, 1.0)
        return final_score, reasons[:5]  # Top 5 reasons
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points in kilometers"""
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Earth's radius in kilometers
        
        return c * r
    
    def _calculate_response_similarity(self, value1, value2):
        """Calculate similarity between two response values"""
        # Exact match
        if value1 == value2:
            return 1.0
        
        # Try to parse as comma-separated multi-select
        try:
            set1 = set(v.strip() for v in value1.split(','))
            set2 = set(v.strip() for v in value2.split(','))
            
            if len(set1) > 1 or len(set2) > 1:
                # Multi-select: Jaccard similarity
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                return intersection / union if union > 0 else 0
        except:
            pass
        
        # Scale/numeric similarity
        try:
            num1 = float(value1)
            num2 = float(value2) 
            max_diff = 5  # Assume scale of 1-5
            diff = abs(num1 - num2)
            return max(0, 1 - (diff / max_diff))
        except:
            pass
        
        # String similarity (basic)
        if value1.lower() in value2.lower() or value2.lower() in value1.lower():
            return 0.5
        
        return 0.1  # Minimal similarity for different responses
    
    def _apply_fairness_filter(self, matches):
        """Apply fairness filtering to prevent homogenization"""
        # This is a simple implementation - in production you might want more sophisticated algorithms
        if len(matches) <= 10:
            return matches
        
        # Select diverse matches (every nth match) to ensure variety
        filtered = []
        step = max(1, len(matches) // 20)  # Select every nth match
        
        for i in range(0, len(matches), step):
            filtered.append(matches[i])
            if len(filtered) >= 20:
                break
        
        return filtered
    
    def _save_match(self, user_id_1, match_data):
        """Save a match to the database"""
        user_id_2 = match_data['user_id']
        
        # Ensure consistent ordering (smaller UUID first)
        if str(user_id_1) > str(user_id_2):
            user_id_1, user_id_2 = user_id_2, user_id_1
        
        query = text("""
            INSERT INTO social_matches (user_id_1, user_id_2, compatibility_score, match_reasons)
            VALUES (:user_id_1, :user_id_2, :score, :reasons)
            ON CONFLICT (user_id_1, user_id_2) DO UPDATE SET
                compatibility_score = EXCLUDED.compatibility_score,
                match_reasons = EXCLUDED.match_reasons,
                updated_at = CURRENT_TIMESTAMP
        """)
        
        db.session.execute(query, {
            'user_id_1': user_id_1,
            'user_id_2': user_id_2,
            'score': match_data['compatibility_score'],
            'reasons': json.dumps(match_data['match_reasons'])
        })

# Register API endpoints
api.add_resource(OnboardingQuestionsApi, '/social/onboarding/questions')
api.add_resource(OnboardingResponsesApi, '/social/onboarding/responses')
api.add_resource(MatchingApi, '/social/matching')

# Additional endpoints would include:
# - EventsApi for event management
# - InvitationsApi for event invitations  
# - MessagesApi for communication
# - ModerationApi for reporting
# - GroupsApi for social groups

if __name__ == '__main__':
    print("222.place Social API endpoints defined")