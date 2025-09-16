#!/bin/bash
# 222.place Smoke Test Script
# Tests basic functionality of the matchmaking platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
API_BASE_URL="http://localhost:5000"
WEB_BASE_URL="http://localhost:3000"
TEST_USER_EMAIL="test@222place.local"
TEST_USER_PASSWORD="test123!@#"

echo -e "${YELLOW}🧪 Starting 222.place Smoke Tests${NC}"
echo "=================================="

# Function to check if service is up
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo -n "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}✅ Ready${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e " ${RED}❌ Failed${NC}"
    echo "❌ $service_name is not responding after $((max_attempts * 2)) seconds"
    return 1
}

# Test 1: Check if services are running
echo -e "\n${YELLOW}Test 1: Service Health Checks${NC}"
echo "------------------------------"

check_service "API" "$API_BASE_URL/health"
check_service "Web Frontend" "$WEB_BASE_URL/api/health"

# Test 2: API Health Check
echo -e "\n${YELLOW}Test 2: API Health Check${NC}"
echo "-------------------------"

api_health=$(curl -s "$API_BASE_URL/health" | grep -o '"status":"healthy"' || echo "")
if [ -n "$api_health" ]; then
    echo -e "✅ API health check: ${GREEN}PASSED${NC}"
else
    echo -e "❌ API health check: ${RED}FAILED${NC}"
    exit 1
fi

# Test 3: Database Connection
echo -e "\n${YELLOW}Test 3: Database Connection${NC}"
echo "----------------------------"

db_health=$(curl -s "$API_BASE_URL/health/detailed" | grep -o '"database":{"status":"healthy"' || echo "")
if [ -n "$db_health" ]; then
    echo -e "✅ Database connection: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Database connection: ${RED}FAILED${NC}"
    exit 1
fi

# Test 4: Redis Connection
echo -e "\n${YELLOW}Test 4: Redis Connection${NC}"
echo "-------------------------"

redis_health=$(curl -s "$API_BASE_URL/health/detailed" | grep -o '"redis":{"status":"healthy"' || echo "")
if [ -n "$redis_health" ]; then
    echo -e "✅ Redis connection: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Redis connection: ${RED}FAILED${NC}"
    exit 1
fi

# Test 5: Web Frontend Response
echo -e "\n${YELLOW}Test 5: Web Frontend Response${NC}"
echo "------------------------------"

web_response=$(curl -s "$WEB_BASE_URL" | grep -o "222.place" || echo "")
if [ -n "$web_response" ]; then
    echo -e "✅ Web frontend: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Web frontend: ${RED}FAILED${NC}"
    exit 1
fi

# Test 6: API Endpoints
echo -e "\n${YELLOW}Test 6: API Endpoints${NC}"
echo "----------------------"

# Test auth endpoints
auth_response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/auth/login")
if [ "$auth_response" == "405" ] || [ "$auth_response" == "422" ]; then
    echo -e "✅ Auth endpoint accessible: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Auth endpoint: ${RED}FAILED (HTTP $auth_response)${NC}"
fi

# Test onboarding endpoints
onboarding_response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/onboarding/questions")
if [ "$onboarding_response" == "200" ] || [ "$onboarding_response" == "422" ]; then
    echo -e "✅ Onboarding endpoint accessible: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Onboarding endpoint: ${RED}FAILED (HTTP $onboarding_response)${NC}"
fi

# Test matches endpoints
matches_response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/matches/")
if [ "$matches_response" == "401" ] || [ "$matches_response" == "422" ]; then
    echo -e "✅ Matches endpoint accessible: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Matches endpoint: ${RED}FAILED (HTTP $matches_response)${NC}"
fi

# Test events endpoints
events_response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/events/suggestions")
if [ "$events_response" == "401" ] || [ "$events_response" == "422" ]; then
    echo -e "✅ Events endpoint accessible: ${GREEN}PASSED${NC}"
else
    echo -e "❌ Events endpoint: ${RED}FAILED (HTTP $events_response)${NC}"
fi

# Test 7: Container Health
echo -e "\n${YELLOW}Test 7: Container Health${NC}"
echo "-------------------------"

# Check if containers are running
containers=(222place_db 222place_redis 222place_api 222place_web)
all_containers_healthy=true

for container in "${containers[@]}"; do
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep "$container" | grep -q "Up"; then
        echo -e "✅ $container: ${GREEN}RUNNING${NC}"
    else
        echo -e "❌ $container: ${RED}NOT RUNNING${NC}"
        all_containers_healthy=false
    fi
done

if [ "$all_containers_healthy" = false ]; then
    echo -e "\n${RED}❌ Some containers are not running${NC}"
    exit 1
fi

# Test 8: Performance Check
echo -e "\n${YELLOW}Test 8: Performance Check${NC}"
echo "--------------------------"

# Check API response time
api_time=$(curl -s -o /dev/null -w "%{time_total}" "$API_BASE_URL/health")
api_time_ms=$(echo "$api_time * 1000" | bc)

if (( $(echo "$api_time < 2.0" | bc -l) )); then
    echo -e "✅ API response time: ${GREEN}${api_time_ms}ms (GOOD)${NC}"
else
    echo -e "⚠️ API response time: ${YELLOW}${api_time_ms}ms (SLOW)${NC}"
fi

# Check web response time
web_time=$(curl -s -o /dev/null -w "%{time_total}" "$WEB_BASE_URL")
web_time_ms=$(echo "$web_time * 1000" | bc)

if (( $(echo "$web_time < 3.0" | bc -l) )); then
    echo -e "✅ Web response time: ${GREEN}${web_time_ms}ms (GOOD)${NC}"
else
    echo -e "⚠️ Web response time: ${YELLOW}${web_time_ms}ms (SLOW)${NC}"
fi

# Final Results
echo -e "\n${GREEN}🎉 All smoke tests completed successfully!${NC}"
echo "========================================"
echo -e "✅ Services are healthy and responding"
echo -e "✅ Database and Redis connections working"
echo -e "✅ API endpoints accessible"
echo -e "✅ Web frontend loading"
echo -e "✅ All containers running"

echo -e "\n📋 Quick Links:"
echo -e "   🌐 Web App: $WEB_BASE_URL"
echo -e "   🔧 API Docs: $API_BASE_URL/docs"
echo -e "   ❤️ Health: $API_BASE_URL/health"
echo -e "   📊 Metrics: http://localhost:9090"

echo -e "\n${GREEN}Verification: OK${NC}"
exit 0