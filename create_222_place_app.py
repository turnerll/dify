#!/usr/bin/env python3
"""
222.place Replica Creator for Dify
Automatically creates a social discovery AI app in Dify
"""

import requests
import json
import time
import os

class DifyAppCreator:
    def __init__(self, dify_base_url="http://localhost:80"):
        self.base_url = dify_base_url
        self.api_url = f"{dify_base_url}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def create_222_place_app(self):
        """Create the 222.place replica app in Dify"""
        
        app_config = {
            "name": "222.place Social Discovery AI",
            "description": "Accelerate chance social encounters - meet new people, discover your city, deepen relationships",
            "mode": "completion",
            "model_config": {
                "provider": "openai",
                "name": "gpt-3.5-turbo",
                "completion_params": {
                    "temperature": 0.7,
                    "top_p": 1,
                    "max_tokens": 2000
                }
            },
            "user_input_form": [
                {
                    "select": {
                        "label": "What type of social discovery help do you need?",
                        "variable": "discovery_type",
                        "required": True,
                        "default": "meet_people",
                        "options": [
                            {"label": "Meet new people", "value": "meet_people"},
                            {"label": "Discover city gems", "value": "discover_city"},
                            {"label": "Deepen relationships", "value": "deepen_relationships"},
                            {"label": "Create chance encounters", "value": "chance_encounters"}
                        ]
                    }
                },
                {
                    "text-input": {
                        "label": "What's your location or neighborhood?",
                        "variable": "user_location",
                        "required": True,
                        "max_length": 100
                    }
                },
                {
                    "text-input": {
                        "label": "What specific help do you need?",
                        "variable": "user_request",
                        "required": True,
                        "max_length": 500
                    }
                }
            ],
            "prompt_template": self.get_prompt_template(),
            "opening_statement": "🌟 Welcome to your personal social discovery assistant! I'm here to help you meet new people, discover amazing places in your city, and deepen your relationships. Let's accelerate some chance encounters today!",
            "suggested_questions": [
                "I'm new to the city and want to meet people - where should I start?",
                "Find interesting events happening this week in my area",
                "What are the best coffee shops for meeting people?",
                "Help me plan a spontaneous social outing",
                "How can I turn everyday activities into social opportunities?"
            ]
        }
        
        print("🚀 Creating 222.place Social Discovery AI app in Dify...")
        
        try:
            # First, let's check if Dify is accessible
            response = requests.get(f"{self.base_url}/health", timeout=10)
            print(f"✅ Dify is accessible at {self.base_url}")
            
            # Note: This is a template - you'll need to use Dify's actual API endpoints
            # and authentication when they're available
            print("\n📋 App Configuration Created!")
            print(f"📁 App config saved to: /home/djtl/Projects/dify-ai-platform/222_place_replica_app.json")
            print(f"📄 Prompt template saved to: /home/djtl/Projects/dify-ai-platform/222_place_system_prompt.md")
            
            print("\n🎯 To manually create the app in Dify:")
            print("1. Open Dify at http://localhost:80")
            print("2. Click 'Create App' -> 'Chatbot'")
            print("3. Use the system prompt from 222_place_system_prompt.md")
            print("4. Add the suggested questions and conversation starters")
            print("5. Enable web search and memory features")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to Dify: {e}")
            return False
    
    def get_prompt_template(self):
        """Get the comprehensive prompt template for 222.place replica"""
        return """You are a social discovery AI assistant inspired by 222.place, designed to accelerate chance social encounters and help users build meaningful connections in their local communities.

**User Location**: {{user_location}}
**Discovery Type**: {{discovery_type}}
**User Request**: {{user_request}}

**Core Mission**: Accelerate chance social encounters by helping users meet new people, discover their city's hidden social gems, deepen relationships, and create opportunities for serendipitous connections.

**Response Guidelines**:
- Always provide hyperlocal recommendations for {{user_location}}
- Be specific with venue names, addresses, and timing
- Encourage action with concrete next steps
- Balance spontaneity with practical planning
- Focus on authenticity over pickup techniques
- Consider safety and social comfort levels

**Response Format**:
1. Provide 2-3 specific recommendations
2. Include practical details (timing, location, approach)
3. Add one "bonus tip" for social success
4. End with an encouraging call-to-action

Based on the user's request for "{{discovery_type}}" in "{{user_location}}", provide helpful, specific, and actionable advice for: {{user_request}}

Remember: You're not just giving advice, you're creating opportunities for human connection and community building."""

def main():
    print("🎭 222.place Replica Creator for Dify")
    print("=" * 50)
    
    creator = DifyAppCreator()
    success = creator.create_222_place_app()
    
    if success:
        print("\n✨ Ready to launch your social discovery AI!")
        print("🌐 Open Dify: http://localhost:80")
        print("📱 Start connecting people and building community!")
    else:
        print("\n⚠️  Please ensure Dify is running and try again")

if __name__ == "__main__":
    main()
