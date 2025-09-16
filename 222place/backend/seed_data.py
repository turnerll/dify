"""
Seed data for 222.place social matching application
"""
import json
from datetime import datetime, timedelta

# Onboarding questions (50-80 questions covering all aspects)
QUESTIONS = [
    # Demographics & Basic Info
    {
        "category": "demographics",
        "question_text_en": "What is your age range?",
        "question_text_es": "¿Cuál es tu rango de edad?",
        "question_type": "multiple_choice",
        "options": ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
        "weight": 0.8
    },
    {
        "category": "demographics",
        "question_text_en": "What city are you located in?",
        "question_text_es": "¿En qué ciudad te encuentras?",
        "question_type": "text",
        "weight": 1.0
    },
    {
        "category": "demographics",
        "question_text_en": "How far are you willing to travel for social activities? (km)",
        "question_text_es": "¿Qué tan lejos estás dispuesto/a a viajar para actividades sociales? (km)",
        "question_type": "multiple_choice",
        "options": ["5", "10", "25", "50", "100+"],
        "weight": 0.9
    },
    {
        "category": "demographics",
        "question_text_en": "What is your preferred language for social interactions?",
        "question_text_es": "¿Cuál es tu idioma preferido para interacciones sociales?",
        "question_type": "multiple_choice",
        "options": ["English", "Spanish", "Both equally", "Other"],
        "weight": 0.7
    },
    
    # Interests & Hobbies
    {
        "category": "interests",
        "question_text_en": "What are your main hobbies and interests? (Select all that apply)",
        "question_text_es": "¿Cuáles son tus principales aficiones e intereses? (Selecciona todas las que apliquen)",
        "question_type": "multi_select",
        "options": [
            "Cooking", "Photography", "Reading", "Hiking", "Music", "Art", "Sports", 
            "Gaming", "Travel", "Technology", "Movies", "Dancing", "Fitness", "Crafts",
            "Gardening", "Writing", "Volunteer Work", "Board Games", "Theater", "Fashion"
        ],
        "weight": 1.0
    },
    {
        "category": "interests",
        "question_text_en": "What type of music do you enjoy?",
        "question_text_es": "¿Qué tipo de música disfrutas?",
        "question_type": "multi_select",
        "options": [
            "Pop", "Rock", "Jazz", "Classical", "Electronic", "Hip-Hop", "Country",
            "Latin", "Reggae", "Folk", "Blues", "Indie", "Metal", "R&B"
        ],
        "weight": 0.6
    },
    {
        "category": "interests",
        "question_text_en": "How do you prefer to spend your free time?",
        "question_text_es": "¿Cómo prefieres pasar tu tiempo libre?",
        "question_type": "multi_select",
        "options": [
            "Outdoor activities", "Indoor activities", "Social gatherings", "Quiet time alone",
            "Learning new skills", "Exercising", "Cultural events", "Spontaneous adventures"
        ],
        "weight": 0.8
    },
    {
        "category": "interests",
        "question_text_en": "What sports or physical activities do you enjoy?",
        "question_text_es": "¿Qué deportes o actividades físicas disfrutas?",
        "question_type": "multi_select",
        "options": [
            "Running", "Swimming", "Cycling", "Tennis", "Soccer", "Basketball", "Yoga",
            "Pilates", "Rock climbing", "Skiing", "Martial arts", "Golf", "None", "Other"
        ],
        "weight": 0.7
    },
    
    # Food & Dining
    {
        "category": "dining",
        "question_text_en": "What type of cuisine do you enjoy most?",
        "question_text_es": "¿Qué tipo de cocina disfrutas más?",
        "question_type": "multi_select",
        "options": [
            "Italian", "Mexican", "Asian", "Mediterranean", "American", "Indian", "French",
            "Thai", "Japanese", "Greek", "Middle Eastern", "Vegetarian", "Vegan", "Fusion"
        ],
        "weight": 0.8
    },
    {
        "category": "dining",
        "question_text_en": "Do you have any dietary restrictions or preferences?",
        "question_text_es": "¿Tienes alguna restricción o preferencia dietética?",
        "question_type": "multi_select",
        "options": [
            "None", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Nut allergies",
            "Halal", "Kosher", "Low-carb", "Keto", "Paleo", "Other food allergies"
        ],
        "weight": 1.0
    },
    {
        "category": "dining",
        "question_text_en": "What's your preferred dining atmosphere?",
        "question_text_es": "¿Cuál es tu ambiente preferido para cenar?",
        "question_type": "multi_select",
        "options": [
            "Casual restaurants", "Fine dining", "Outdoor patios", "Cozy cafes",
            "Food trucks", "Home cooking", "Buffets", "Ethnic restaurants"
        ],
        "weight": 0.7
    },
    {
        "category": "dining",
        "question_text_en": "How often do you like to try new restaurants?",
        "question_text_es": "¿Con qué frecuencia te gusta probar nuevos restaurantes?",
        "question_type": "multiple_choice",
        "options": ["Weekly", "Monthly", "Occasionally", "Rarely", "I prefer familiar places"],
        "weight": 0.6
    },
    
    # Social Preferences
    {
        "category": "social",
        "question_text_en": "What size group do you prefer for social activities?",
        "question_text_es": "¿Qué tamaño de grupo prefieres para actividades sociales?",
        "question_type": "multiple_choice",
        "options": ["1-on-1", "Small groups (3-5)", "Medium groups (6-10)", "Large groups (10+)", "No preference"],
        "weight": 0.9
    },
    {
        "category": "social",
        "question_text_en": "How would you describe your personality in social settings?",
        "question_text_es": "¿Cómo describirías tu personalidad en entornos sociales?",
        "question_type": "multiple_choice",
        "options": ["Very outgoing", "Somewhat outgoing", "Balanced", "Somewhat reserved", "Very reserved"],
        "weight": 0.8
    },
    {
        "category": "social",
        "question_text_en": "What type of conversations do you enjoy most?",
        "question_text_es": "¿Qué tipo de conversaciones disfrutas más?",
        "question_type": "multi_select",
        "options": [
            "Deep philosophical discussions", "Light-hearted chat", "Current events", "Personal stories",
            "Professional topics", "Creative ideas", "Humor and jokes", "Cultural topics"
        ],
        "weight": 0.7
    },
    {
        "category": "social",
        "question_text_en": "How do you prefer to meet new people?",
        "question_text_es": "¿Cómo prefieres conocer gente nueva?",
        "question_type": "multi_select",
        "options": [
            "Through mutual friends", "At organized events", "In hobby/interest groups",
            "Through work", "Online platforms", "Spontaneous encounters", "Community activities"
        ],
        "weight": 0.6
    },
    
    # Availability & Schedule
    {
        "category": "availability",
        "question_text_en": "What days of the week are you typically available for social activities?",
        "question_text_es": "¿Qué días de la semana sueles estar disponible para actividades sociales?",
        "question_type": "multi_select",
        "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "weight": 1.0
    },
    {
        "category": "availability",
        "question_text_en": "What time of day do you prefer for social activities?",
        "question_text_es": "¿A qué hora del día prefieres las actividades sociales?",
        "question_type": "multi_select",
        "options": ["Early morning", "Late morning", "Afternoon", "Early evening", "Late evening", "Night"],
        "weight": 0.8
    },
    {
        "category": "availability",
        "question_text_en": "How much advance notice do you prefer for plans?",
        "question_text_es": "¿Con cuánta anticipación prefieres que te avisen de los planes?",
        "question_type": "multiple_choice",
        "options": ["Same day", "1-2 days", "3-7 days", "1-2 weeks", "1+ month"],
        "weight": 0.6
    },
    {
        "category": "availability",
        "question_text_en": "How often would you like to participate in social activities?",
        "question_text_es": "¿Con qué frecuencia te gustaría participar en actividades sociales?",
        "question_type": "multiple_choice",
        "options": ["Daily", "Several times a week", "Weekly", "Bi-weekly", "Monthly", "Occasionally"],
        "weight": 0.7
    },
    
    # Budget & Financial
    {
        "category": "budget",
        "question_text_en": "What's your typical budget for a dinner out?",
        "question_text_es": "¿Cuál es tu presupuesto típico para cenar fuera?",
        "question_type": "multiple_choice",
        "options": ["Under $20", "$20-40", "$40-60", "$60-100", "Over $100", "Budget varies by occasion"],
        "weight": 0.9
    },
    {
        "category": "budget",
        "question_text_en": "What's your budget range for entertainment activities?",
        "question_text_es": "¿Cuál es tu rango de presupuesto para actividades de entretenimiento?",
        "question_type": "multiple_choice",
        "options": ["Under $30", "$30-50", "$50-100", "$100-200", "Over $200", "Flexible"],
        "weight": 0.8
    },
    {
        "category": "budget",
        "question_text_en": "How do you prefer to handle bill splitting?",
        "question_text_es": "¿Cómo prefieres dividir la cuenta?",
        "question_type": "multiple_choice",
        "options": ["Split evenly", "Pay for what you ordered", "Take turns paying", "Someone treats", "Flexible"],
        "weight": 0.6
    },
    
    # Transportation & Accessibility
    {
        "category": "accessibility",
        "question_text_en": "What is your primary mode of transportation?",
        "question_text_es": "¿Cuál es tu principal medio de transporte?",
        "question_type": "multiple_choice",
        "options": ["Car", "Public transit", "Walking", "Bicycle", "Rideshare/Taxi", "Motorcycle", "Combination"],
        "weight": 0.7
    },
    {
        "category": "accessibility",
        "question_text_en": "Do you have any accessibility needs we should consider?",
        "question_text_es": "¿Tienes alguna necesidad de accesibilidad que debamos considerar?",
        "question_type": "multi_select",
        "options": [
            "None", "Wheelchair accessible venues", "Hearing assistance", "Visual assistance",
            "Service animal accommodation", "Step-free access", "Accessible parking", "Other"
        ],
        "weight": 1.0
    },
    {
        "category": "accessibility",
        "question_text_en": "Are you comfortable with venues that serve alcohol?",
        "question_text_es": "¿Te sientes cómodo/a en lugares que sirven alcohol?",
        "question_type": "multiple_choice",
        "options": ["Yes, I drink", "Yes, but I don't drink", "Prefer alcohol-free venues", "No preference"],
        "weight": 0.5
    },
    
    # Cultural & Values
    {
        "category": "culture",
        "question_text_en": "What cultural backgrounds are you interested in learning about?",
        "question_text_es": "¿Qué antecedentes culturales te interesa conocer?",
        "question_type": "multi_select",
        "options": [
            "Latin American", "Asian", "European", "African", "Middle Eastern", "Indigenous",
            "Caribbean", "Pacific Islander", "North American", "All cultures", "My own culture"
        ],
        "weight": 0.6
    },
    {
        "category": "culture",
        "question_text_en": "What values are most important to you in friendships?",
        "question_text_es": "¿Qué valores son más importantes para ti en las amistades?",
        "question_type": "multi_select",
        "options": [
            "Honesty", "Loyalty", "Humor", "Kindness", "Reliability", "Open-mindedness",
            "Respect", "Shared interests", "Emotional support", "Adventure", "Intellectual stimulation"
        ],
        "weight": 0.8
    },
    {
        "category": "culture",
        "question_text_en": "How important is it that others share your political views?",
        "question_text_es": "¿Qué tan importante es que otros compartan tus puntos de vista políticos?",
        "question_type": "multiple_choice",
        "options": ["Very important", "Somewhat important", "Not very important", "Not important at all", "Prefer not to discuss"],
        "weight": 0.4
    },
    {
        "category": "culture",
        "question_text_en": "How important is it that others share your religious/spiritual beliefs?",
        "question_text_es": "¿Qué tan importante es que otros compartan tus creencias religiosas/espirituales?",
        "question_type": "multiple_choice",
        "options": ["Very important", "Somewhat important", "Not very important", "Not important at all", "Prefer not to discuss"],
        "weight": 0.4
    },
    
    # Activities & Events
    {
        "category": "activities",
        "question_text_en": "What types of group activities interest you most?",
        "question_text_es": "¿Qué tipos de actividades grupales te interesan más?",
        "question_type": "multi_select",
        "options": [
            "Dinner parties", "Game nights", "Outdoor adventures", "Cultural events", "Sports events",
            "Concerts/Shows", "Workshops/Classes", "Volunteer activities", "Travel/Trips", "Networking events"
        ],
        "weight": 1.0
    },
    {
        "category": "activities",
        "question_text_en": "What types of events would you be interested in attending?",
        "question_text_es": "¿A qué tipos de eventos te interesaría asistir?",
        "question_type": "multi_select",
        "options": [
            "Football games", "Basketball games", "Baseball games", "Soccer matches", "Tennis matches",
            "Concerts", "Theater shows", "Comedy shows", "Art exhibitions", "Food festivals",
            "Street fairs", "Farmers markets", "Wine tastings", "Beer festivals"
        ],
        "weight": 0.9
    },
    {
        "category": "activities",
        "question_text_en": "How do you feel about trying new activities?",
        "question_text_es": "¿Cómo te sientes acerca de probar nuevas actividades?",
        "question_type": "multiple_choice",
        "options": ["Love trying new things", "Open to new experiences", "Prefer familiar activities", "Cautious about new things"],
        "weight": 0.6
    },
    
    # Communication & Technology
    {
        "category": "communication",
        "question_text_en": "How do you prefer to communicate when planning events?",
        "question_text_es": "¿Cómo prefieres comunicarte al planificar eventos?",
        "question_type": "multi_select",
        "options": ["Text messages", "Phone calls", "Email", "App notifications", "In-person", "Video calls"],
        "weight": 0.5
    },
    {
        "category": "communication",
        "question_text_en": "How comfortable are you with sharing personal information?",
        "question_text_es": "¿Qué tan cómodo/a te sientes compartiendo información personal?",
        "question_type": "multiple_choice",
        "options": ["Very open", "Somewhat open", "Selective sharing", "Private", "Very private"],
        "weight": 0.6
    },
    
    # Lifestyle & Personal
    {
        "category": "lifestyle",
        "question_text_en": "What's your work/life balance preference?",
        "question_text_es": "¿Cuál es tu preferencia de equilibrio trabajo/vida?",
        "question_type": "multiple_choice",
        "options": ["Work-focused", "Balanced", "Life-focused", "Flexible", "Varies by season"],
        "weight": 0.5
    },
    {
        "category": "lifestyle",
        "question_text_en": "Do you have any pets?",
        "question_text_es": "¿Tienes mascotas?",
        "question_type": "multiple_choice",
        "options": ["Dogs", "Cats", "Other pets", "No pets", "Multiple pets"],
        "weight": 0.3
    },
    {
        "category": "lifestyle",
        "question_text_en": "What's your living situation?",
        "question_text_es": "¿Cuál es tu situación de vivienda?",
        "question_type": "multiple_choice",
        "options": ["Live alone", "With roommates", "With family", "With partner", "Other"],
        "weight": 0.3
    },
    {
        "category": "lifestyle",
        "question_text_en": "How would you describe your current life stage?",
        "question_text_es": "¿Cómo describirías tu etapa actual de vida?",
        "question_type": "multiple_choice",
        "options": ["Student", "Early career", "Established career", "Career change", "Retired", "Other"],
        "weight": 0.6
    }
]

# Sample users for testing
SAMPLE_USERS = [
    {
        "email": "maria.garcia@example.com",
        "name": "Maria Garcia",
        "display_name": "Maria",
        "bio": "Love exploring new restaurants and cultural events. Always up for good conversation!",
        "location_city": "San Francisco",
        "location_lat": 37.7749,
        "location_lng": -122.4194,
        "preferred_language": "es"
    },
    {
        "email": "john.smith@example.com", 
        "name": "John Smith",
        "display_name": "John",
        "bio": "Tech enthusiast who enjoys hiking and trying new cuisines. Looking for adventure buddies!",
        "location_city": "San Francisco",
        "location_lat": 37.7849,
        "location_lng": -122.4094,
        "preferred_language": "en"
    },
    {
        "email": "sofia.rodriguez@example.com",
        "name": "Sofia Rodriguez", 
        "display_name": "Sofia",
        "bio": "Artist and foodie. I speak both English and Spanish fluently.",
        "location_city": "Oakland",
        "location_lat": 37.8044,
        "location_lng": -122.2711,
        "preferred_language": "en"
    },
    {
        "email": "alex.chen@example.com",
        "name": "Alex Chen",
        "display_name": "Alex", 
        "bio": "Photographer who loves concerts and outdoor activities. Always looking for new friends!",
        "location_city": "Berkeley",
        "location_lat": 37.8715,
        "location_lng": -122.2730,
        "preferred_language": "en"
    },
    {
        "email": "admin@222place.com",
        "name": "222place Admin",
        "display_name": "Admin",
        "bio": "System administrator for testing purposes",
        "location_city": "San Francisco",
        "location_lat": 37.7749,
        "location_lng": -122.4194,
        "preferred_language": "en"
    }
]

# Sample events
SAMPLE_EVENTS = [
    {
        "title": "Weekend Dinner at Italian Bistro",
        "description": "Join us for authentic Italian cuisine in North Beach. Great for food lovers!",
        "event_type": "dinner",
        "venue_name": "Mama's Italian Kitchen",
        "venue_address": "123 Columbus Ave, San Francisco, CA",
        "venue_lat": 37.7983,
        "venue_lng": -122.4078,
        "max_participants": 6,
        "budget_min": 25.00,
        "budget_max": 45.00,
        "dietary_accommodations": ["vegetarian", "gluten-free"],
        "language_preference": "en"
    },
    {
        "title": "Picnic and Football Game Viewing",
        "description": "Casual gathering to watch the game with snacks and good company!",
        "event_type": "outing",
        "venue_name": "Golden Gate Park",
        "venue_address": "Golden Gate Park, San Francisco, CA",
        "venue_lat": 37.7694,
        "venue_lng": -122.4862,
        "max_participants": 12,
        "budget_min": 10.00,
        "budget_max": 20.00,
        "language_preference": "en"
    },
    {
        "title": "Concert Night at the Fillmore",
        "description": "Live music and dancing! Perfect for music lovers.",
        "event_type": "outing",
        "venue_name": "The Fillmore",
        "venue_address": "1805 Geary Blvd, San Francisco, CA",
        "venue_lat": 37.7844,
        "venue_lng": -122.4332,
        "max_participants": 8,
        "budget_min": 40.00,
        "budget_max": 80.00,
        "language_preference": "en"
    },
    {
        "title": "Noche de Tacos y Conversación",
        "description": "Una noche relajada para disfrutar tacos auténticos y buena conversación en español.",
        "event_type": "dinner",
        "venue_name": "Tacos El Farolito",
        "venue_address": "2779 Mission St, San Francisco, CA",
        "venue_lat": 37.7531,
        "venue_lng": -122.4188,
        "max_participants": 8,
        "budget_min": 15.00,
        "budget_max": 25.00,
        "dietary_accommodations": ["vegetarian"],
        "language_preference": "es"
    }
]

def get_questions():
    """Return the list of onboarding questions"""
    return QUESTIONS

def get_sample_users():
    """Return sample users for testing"""
    return SAMPLE_USERS

def get_sample_events():
    """Return sample events"""
    return SAMPLE_EVENTS

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} onboarding questions")
    print(f"Loaded {len(SAMPLE_USERS)} sample users")
    print(f"Loaded {len(SAMPLE_EVENTS)} sample events")
    
    # Print question categories
    categories = {}
    for q in QUESTIONS:
        cat = q["category"]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    print("\nQuestion categories:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} questions")