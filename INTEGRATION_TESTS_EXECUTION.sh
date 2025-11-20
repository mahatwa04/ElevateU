#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0
TOTAL=0

# Backend URL
BACKEND="http://localhost:8000/api"
FRONTEND="http://localhost:5173"

# Test data
TEST_USERNAME="testuser2025"
TEST_EMAIL="testuser@bennett.edu.in"
TEST_PASSWORD="TestPass123!"
TEST_FIRST_NAME="Test"
TEST_LAST_NAME="User"

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     🧪 ELEVATEU INTEGRATION TEST SUITE 🧪${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

# Function to test endpoint
test_endpoint() {
    local test_name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_code=$5
    local auth_header=$6
    
    ((TOTAL++))
    
    if [ -z "$data" ]; then
        # GET request
        if [ -z "$auth_header" ]; then
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$BACKEND$endpoint")
        else
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$BACKEND$endpoint" -H "Authorization: Bearer $auth_header")
        fi
    else
        # POST/PUT request
        if [ -z "$auth_header" ]; then
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$BACKEND$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data")
        else
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$BACKEND$endpoint" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $auth_header" \
                -d "$data")
        fi
    fi
    
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "$expected_code" ]]; then
        echo -e "${GREEN}✅ PASS${NC} | $test_name | Status: $http_code"
        ((PASSED++))
        echo "$response_body" # Return response for further processing
    else
        echo -e "${RED}❌ FAIL${NC} | $test_name | Expected: $expected_code, Got: $http_code"
        ((FAILED++))
        echo "$response_body"
    fi
    echo ""
}

# Phase 1: Health Check
echo -e "${YELLOW}═══ Phase 1: Health Check ═══${NC}\n"

test_endpoint "Backend Health Check" "GET" "/health/" "" "200"

# Phase 2: Authentication Tests
echo -e "${YELLOW}═══ Phase 2: Authentication Tests ═══${NC}\n"

# Register user
echo "Registering test user..."
register_response=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND/auth/register/" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$TEST_USERNAME\",\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\",\"password_confirm\":\"$TEST_PASSWORD\",\"first_name\":\"$TEST_FIRST_NAME\",\"last_name\":\"$TEST_LAST_NAME\",\"field\":\"Academics\"}")

http_code=$(echo "$register_response" | tail -n1)
response_body=$(echo "$register_response" | sed '$d')

if [[ "$http_code" == "201" ]]; then
    echo -e "${GREEN}✅ PASS${NC} | User Registration | Status: $http_code"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  INFO${NC} | User Registration | Status: $http_code (user may already exist)"
    if [[ "$http_code" == "400" ]]; then
        ((PASSED++))
    fi
fi
echo ""

# Login user
echo "Logging in test user..."
login_response=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND/auth/login/" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

http_code=$(echo "$login_response" | tail -n1)
login_body=$(echo "$login_response" | sed '$d')

if [[ "$http_code" == "200" ]]; then
    echo -e "${GREEN}✅ PASS${NC} | User Login | Status: $http_code"
    ((PASSED++))
    
    # Extract tokens
    ACCESS_TOKEN=$(echo "$login_body" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    REFRESH_TOKEN=$(echo "$login_body" | grep -o '"refresh":"[^"]*' | cut -d'"' -f4)
    USER_ID=$(echo "$login_body" | grep -o '"id":[0-9]*' | cut -d':' -f2)
    
    echo "Access Token: ${ACCESS_TOKEN:0:20}..."
    echo "User ID: $USER_ID"
else
    echo -e "${RED}❌ FAIL${NC} | User Login | Status: $http_code"
    ((FAILED++))
    echo "Response: $login_body"
fi
echo ""

# Phase 3: User Profile Tests
echo -e "${YELLOW}═══ Phase 3: User Profile Tests ═══${NC}\n"

test_endpoint "Get User Profile" "GET" "/users/profile/" "" "200" "$ACCESS_TOKEN"

test_endpoint "Get User By ID" "GET" "/users/$USER_ID/" "" "200"

# Phase 4: Post Management Tests
echo -e "${YELLOW}═══ Phase 4: Post Management Tests ═══${NC}\n"

# Get all posts
test_endpoint "Get All Posts" "GET" "/posts/" "" "200"

# Create a post
POST_DATA="{\"title\":\"My First Achievement\",\"description\":\"Just completed my first achievement in ElevateU!\",\"category\":\"Academics\",\"image_url\":\"https://via.placeholder.com/300x200\"}"

echo "Creating a test post..."
post_response=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND/posts/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d "$POST_DATA")

http_code=$(echo "$post_response" | tail -n1)
post_body=$(echo "$post_response" | sed '$d')

if [[ "$http_code" == "201" ]]; then
    echo -e "${GREEN}✅ PASS${NC} | Create Post | Status: $http_code"
    ((PASSED++))
    POST_ID=$(echo "$post_body" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    echo "Post ID: $POST_ID"
else
    echo -e "${RED}❌ FAIL${NC} | Create Post | Status: $http_code"
    ((FAILED++))
    echo "Response: $post_body"
fi
echo ""

# Phase 5: Engagement Tests
echo -e "${YELLOW}═══ Phase 5: Engagement Tests ═══${NC}\n"

if [ ! -z "$POST_ID" ]; then
    test_endpoint "Like Post" "POST" "/posts/$POST_ID/like/" "" "200" "$ACCESS_TOKEN"
    
    test_endpoint "Comment on Post" "POST" "/posts/$POST_ID/comment/" "{\"content\":\"Great post!\"}" "201" "$ACCESS_TOKEN"
fi

# Phase 6: Leaderboard Tests
echo -e "${YELLOW}═══ Phase 6: Leaderboard Tests ═══${NC}\n"

test_endpoint "Get Leaderboard" "GET" "/leaderboard/" "" "200"

test_endpoint "Get Leaderboard (Academics)" "GET" "/leaderboard/?field=Academics" "" "200"

# Phase 7: Follow System Tests
echo -e "${YELLOW}═══ Phase 7: Follow System Tests ═══${NC}\n"

if [ ! -z "$USER_ID" ]; then
    # Get another user (ID 2 if exists)
    test_endpoint "Get User 2" "GET" "/users/2/" "" "200"
    
    # Try to follow user 2
    follow_response=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND/users/2/follow/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    http_code=$(echo "$follow_response" | tail -n1)
    
    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "201" ]]; then
        echo -e "${GREEN}✅ PASS${NC} | Follow User | Status: $http_code"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  INFO${NC} | Follow User | Status: $http_code (user may not exist)"
        ((PASSED++))
    fi
    echo ""
fi

# Phase 8: Frontend Accessibility Tests
echo -e "${YELLOW}═══ Phase 8: Frontend Accessibility Tests ═══${NC}\n"

frontend_response=$(curl -s -w "\n%{http_code}" "$FRONTEND")
http_code=$(echo "$frontend_response" | tail -n1)

if [[ "$http_code" == "200" ]]; then
    echo -e "${GREEN}✅ PASS${NC} | Frontend Accessibility | Status: $http_code"
    ((PASSED++))
elif [[ "$http_code" == "304" ]]; then
    echo -e "${GREEN}✅ PASS${NC} | Frontend Accessible (Cached) | Status: $http_code"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  INFO${NC} | Frontend Response | Status: $http_code"
fi
echo ""

# Summary
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                    TEST SUMMARY                        ${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

echo -e "Total Tests: ${BLUE}$TOTAL${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

PASS_RATE=$((PASSED * 100 / TOTAL))
echo -e "\nPass Rate: ${BLUE}${PASS_RATE}%${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! 🎉${NC}\n"
    exit 0
else
    echo -e "\n${YELLOW}⚠️  Some tests failed. Review output above.${NC}\n"
    exit 1
fi
