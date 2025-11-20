#!/bin/bash
# ElevateU Production Deployment Verification Script
# Run this after deployment to verify everything is working

set -e

BACKEND_URL="https://elevateu-backend.onrender.com"
FRONTEND_URL="https://elevateu.vercel.app"
API_URL="$BACKEND_URL/api"

echo "════════════════════════════════════════════════════════"
echo "🚀 ElevateU Production Deployment Verification"
echo "════════════════════════════════════════════════════════"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local expected_code=$4
    local data=$5
    
    echo -n "Testing: $name... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (Expected $expected_code, got $http_code)"
        FAILED=$((FAILED + 1))
    fi
}

echo "═══════════════════════════════════════════════════════"
echo "🔍 BACKEND API TESTS"
echo "═══════════════════════════════════════════════════════"
echo ""

# Test health endpoint
test_endpoint "Health Check" "GET" "$API_URL/health/" "200"

# Test login endpoint
test_endpoint "Login Endpoint" "POST" "$API_URL/auth/login/" "200" \
    '{"email":"admin@bennett.edu.in","password":"admin123456"}'

# Test posts list
test_endpoint "Posts Endpoint" "GET" "$API_URL/posts/" "200"

# Test leaderboard
test_endpoint "Leaderboard Endpoint" "GET" "$API_URL/engagement/leaderboard/" "200"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "🌐 FRONTEND VERIFICATION"
echo "═══════════════════════════════════════════════════════"
echo ""

echo -n "Testing: Frontend URL... "
frontend_code=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")
if [ "$frontend_code" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $frontend_code)"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $frontend_code)"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📊 CONNECTIVITY TESTS"
echo "═══════════════════════════════════════════════════════"
echo ""

echo -n "Testing: Backend DNS Resolution... "
if nslookup elevateu-backend.onrender.com > /dev/null 2>&1 || \
   host elevateu-backend.onrender.com > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

echo -n "Testing: Frontend DNS Resolution... "
if nslookup elevateu.vercel.app > /dev/null 2>&1 || \
   host elevateu.vercel.app > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "🔐 SECURITY CHECKS"
echo "═══════════════════════════════════════════════════════"
echo ""

echo -n "Testing: HTTPS Backend... "
if curl -s --head "$BACKEND_URL" | grep -q "HTTP.*200\|HTTP.*30"; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

echo -n "Testing: HTTPS Frontend... "
if curl -s --head "$FRONTEND_URL" | grep -q "HTTP.*200\|HTTP.*30"; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📈 RESULTS"
echo "═══════════════════════════════════════════════════════"
echo ""

echo "Tests Passed: $PASSED"
echo "Tests Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! Deployment verified!${NC}"
    echo ""
    echo "Production URLs:"
    echo "- Frontend: $FRONTEND_URL"
    echo "- Backend: $API_URL"
    echo "- Admin: $BACKEND_URL/admin"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check the issues above.${NC}"
    exit 1
fi
