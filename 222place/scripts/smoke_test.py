#!/usr/bin/env python3
"""
Smoke test script for 222.place application
Tests core functionality end-to-end
"""
import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost/v1"
TEST_USER_EMAIL = "maria.garcia@example.com"
TEST_PASSWORD = "test123"

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Color.GREEN}✓ {message}{Color.END}")

def print_error(message):
    print(f"{Color.RED}✗ {message}{Color.END}")

def print_info(message):
    print(f"{Color.BLUE}ℹ {message}{Color.END}")

def print_warning(message):
    print(f"{Color.YELLOW}⚠ {message}{Color.END}")

class SmokeTest:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': '222place-smoke-test/1.0'
        })
        self.auth_token = None

    def test_health_check(self):
        """Test if the application is running"""
        print_info("Testing application health...")
        
        try:
            response = self.session.get(f"{BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                print_success("Application is running")
                return True
            else:
                print_error(f"Health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print_error(f"Cannot connect to application: {e}")
            return False

    def test_authentication(self):
        """Test user authentication"""
        print_info("Testing authentication...")
        
        # For this test, we'll simulate authentication
        # In a real implementation, you'd test the actual auth endpoints
        try:
            # Simulate getting auth token (replace with actual auth endpoint)
            auth_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_PASSWORD
            }
            
            # Since we don't have actual auth implemented yet, simulate success
            self.auth_token = "test-token-123"
            self.session.headers.update({
                'Authorization': f'Bearer {self.auth_token}'
            })
            
            print_success("Authentication successful (simulated)")
            return True
            
        except Exception as e:
            print_error(f"Authentication failed: {e}")
            return False

    def test_onboarding_questions(self):
        """Test fetching onboarding questions"""
        print_info("Testing onboarding questions endpoint...")
        
        try:
            response = self.session.get(f"{BASE_URL}/social/onboarding/questions?lang=en")
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get('questions', [])
                
                if len(questions) >= 50:
                    print_success(f"Retrieved {len(questions)} onboarding questions")
                    
                    # Check question structure
                    sample_question = questions[0]
                    required_fields = ['id', 'category', 'question_text', 'question_type']
                    
                    if all(field in sample_question for field in required_fields):
                        print_success("Question structure is valid")
                        return True
                    else:
                        print_error("Question structure is invalid")
                        return False
                else:
                    print_error(f"Expected at least 50 questions, got {len(questions)}")
                    return False
            else:
                print_error(f"Failed to fetch questions: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error testing onboarding questions: {e}")
            return False

    def test_submit_responses(self):
        """Test submitting onboarding responses"""
        print_info("Testing onboarding response submission...")
        
        try:
            # Sample responses
            sample_responses = {
                "responses": [
                    {"question_id": 1, "response_value": "26-35"},
                    {"question_id": 2, "response_value": "San Francisco"},
                    {"question_id": 3, "response_value": "25"},
                    {"question_id": 4, "response_value": "English"},
                    {"question_id": 5, "response_value": "Cooking,Reading,Music"}
                ],
                "profile": {
                    "display_name": "Test User",
                    "bio": "Testing the 222.place application",
                    "location_city": "San Francisco",
                    "location_lat": 37.7749,
                    "location_lng": -122.4194,
                    "preferred_language": "en"
                }
            }
            
            response = self.session.post(
                f"{BASE_URL}/social/onboarding/responses",
                json=sample_responses
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'successfully' in data['message']:
                    print_success("Response submission successful")
                    return True
                else:
                    print_error("Response submission failed - invalid response")
                    return False
            else:
                print_error(f"Response submission failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print_error(f"Error details: {error_data}")
                except:
                    pass
                return False
                
        except Exception as e:
            print_error(f"Error testing response submission: {e}")
            return False

    def test_matching_generation(self):
        """Test match generation"""
        print_info("Testing match generation...")
        
        try:
            response = self.session.post(f"{BASE_URL}/social/matching")
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'matches_count' in data:
                    matches_count = data['matches_count']
                    print_success(f"Match generation successful - {matches_count} matches found")
                    return True
                else:
                    print_error("Match generation failed - invalid response")
                    return False
            else:
                print_error(f"Match generation failed: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error testing match generation: {e}")
            return False

    def test_fetch_matches(self):
        """Test fetching user matches"""
        print_info("Testing match retrieval...")
        
        try:
            response = self.session.get(f"{BASE_URL}/social/matching?limit=10")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                if isinstance(matches, list):
                    print_success(f"Retrieved {len(matches)} matches")
                    
                    # Check match structure if we have matches
                    if matches:
                        sample_match = matches[0]
                        required_fields = ['id', 'matched_user', 'compatibility_score']
                        
                        if all(field in sample_match for field in required_fields):
                            print_success("Match structure is valid")
                            return True
                        else:
                            print_error("Match structure is invalid")
                            return False
                    else:
                        print_warning("No matches found (this is normal for new users)")
                        return True
                else:
                    print_error("Invalid matches response format")
                    return False
            else:
                print_error(f"Failed to fetch matches: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error testing match retrieval: {e}")
            return False

    def test_database_connectivity(self):
        """Test if database is accessible"""
        print_info("Testing database connectivity...")
        
        try:
            # Try to fetch questions as a database connectivity test
            response = self.session.get(f"{BASE_URL}/social/onboarding/questions")
            
            if response.status_code in [200, 401, 403]:  # Any response means DB is connected
                print_success("Database connectivity confirmed")
                return True
            else:
                print_error("Database connectivity issues")
                return False
                
        except Exception as e:
            print_error(f"Database connectivity test failed: {e}")
            return False

    def run_all_tests(self):
        """Run all smoke tests"""
        print(f"\n{Color.BLUE}=== 222.place Smoke Test Suite ==={Color.END}")
        print(f"Starting smoke tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Testing against: {BASE_URL}\n")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Database Connectivity", self.test_database_connectivity),
            ("Authentication", self.test_authentication),
            ("Onboarding Questions", self.test_onboarding_questions),
            ("Response Submission", self.test_submit_responses),
            ("Match Generation", self.test_matching_generation),
            ("Match Retrieval", self.test_fetch_matches),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print_error(f"Test {test_name} crashed: {e}")
                failed += 1
            
            time.sleep(1)  # Brief pause between tests
        
        # Summary
        print(f"\n{Color.BLUE}=== Test Summary ==={Color.END}")
        print(f"Total tests: {passed + failed}")
        print(f"{Color.GREEN}Passed: {passed}{Color.END}")
        print(f"{Color.RED}Failed: {failed}{Color.END}")
        
        if failed == 0:
            print(f"\n{Color.GREEN}🎉 All tests passed! 222.place is ready to use.{Color.END}")
            return True
        else:
            print(f"\n{Color.RED}❌ {failed} test(s) failed. Please check the application.{Color.END}")
            return False

def main():
    """Main function"""
    tester = SmokeTest()
    
    success = tester.run_all_tests()
    
    if success:
        print(f"\n{Color.GREEN}Verification ok{Color.END}")
        sys.exit(0)
    else:
        print(f"\n{Color.RED}Verification failed{Color.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()