#!/bin/bash

# ElevateU Backend API Testing Script
# Run this after starting: python manage.py runserver

BASE_URL="http://localhost:8000/api"
HEADERS_JSON="Content-Type: application/json"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== ElevateU Backend API Testing ===${NC}\n"

# 1. Register User
echo -e "${GREEN}1. REGISTER USER${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "$HEADERS_JSON" \
  -d '{
    "username": "testuser",
    "email": "testuser@bennett.edu.in",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "field_of_interest": "academics",
    "first_name": "Test",
    "last_name": "User"
  }')

echo "$REGISTER_RESPONSE" | jq .
USER_ID=$(echo "$REGISTER_RESPONSE" | jq '.user.id')
echo ""

# 2. Extract OTP from console output
echo -e "${GREEN}2. VERIFY EMAIL (You'll see OTP in console output above)${NC}"
echo "Copy the OTP from the console email output and replace '123456' below"
OTP="123456"  # Replace with actual OTP

VERIFY_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/verify-email/" \
  -H "$HEADERS_JSON" \
  -d "{
    \"email\": \"testuser@bennett.edu.in\",
    \"otp_code\": \"$OTP\"
  }")

echo "$VERIFY_RESPONSE" | jq .
ACCESS_TOKEN=$(echo "$VERIFY_RESPONSE" | jq -r '.access')
REFRESH_TOKEN=$(echo "$VERIFY_RESPONSE" | jq -r '.refresh')
echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"
echo ""

# 3. Login
echo -e "${GREEN}3. LOGIN${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/token/" \
  -H "$HEADERS_JSON" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }')

echo "$LOGIN_RESPONSE" | jq .
echo ""

# 4. Get Current User Profile
echo -e "${GREEN}4. GET CURRENT USER PROFILE${NC}"
curl -s -X GET "$BASE_URL/users/profile/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 5. Update User Profile
echo -e "${GREEN}5. UPDATE USER PROFILE${NC}"
curl -s -X PUT "$BASE_URL/users/profile/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d '{
    "bio": "Testing ElevateU API",
    "field_of_interest": "tech"
  }' | jq .
echo ""

# 6. Create a Post
echo -e "${GREEN}6. CREATE POST${NC}"
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/posts/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d '{
    "title": "Got A* in Database!",
    "description": "Studied hard for 3 months. Finally got the grade!",
    "category": "academics",
    "image": "https://via.placeholder.com/300"
  }')

echo "$POST_RESPONSE" | jq .
POST_ID=$(echo "$POST_RESPONSE" | jq '.id')
echo "Post ID: $POST_ID"
echo ""

# 7. Get All Posts
echo -e "${GREEN}7. GET ALL POSTS${NC}"
curl -s -X GET "$BASE_URL/posts/" \
  -H "$HEADERS_JSON" | jq '.[] | {id, title, user, like_count, comment_count}' | head -20
echo ""

# 8. Get Post Details
echo -e "${GREEN}8. GET POST DETAILS${NC}"
curl -s -X GET "$BASE_URL/posts/$POST_ID/" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 9. Like a Post
echo -e "${GREEN}9. LIKE POST${NC}"
LIKE_RESPONSE=$(curl -s -X POST "$BASE_URL/engagement/likes/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d "{
    \"post\": $POST_ID
  }")

echo "$LIKE_RESPONSE" | jq .
LIKE_ID=$(echo "$LIKE_RESPONSE" | jq '.id' 2>/dev/null)
echo ""

# 10. Add Comment
echo -e "${GREEN}10. ADD COMMENT${NC}"
COMMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/engagement/comments/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d "{
    \"post\": $POST_ID,
    \"text\": \"Amazing achievement! Congratulations!\"
  }")

echo "$COMMENT_RESPONSE" | jq .
COMMENT_ID=$(echo "$COMMENT_RESPONSE" | jq '.id' 2>/dev/null)
echo ""

# 11. Get Post Comments
echo -e "${GREEN}11. GET POST COMMENTS${NC}"
curl -s -X GET "$BASE_URL/engagement/comments/?post_id=$POST_ID" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 12. Update Comment
echo -e "${GREEN}12. UPDATE COMMENT${NC}"
if [ ! -z "$COMMENT_ID" ] && [ "$COMMENT_ID" != "null" ]; then
  curl -s -X PUT "$BASE_URL/engagement/comments/$COMMENT_ID/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "$HEADERS_JSON" \
    -d '{
      "text": "Updated comment: Amazing achievement! Proud of you!"
    }' | jq .
else
  echo "Comment ID not found, skipping"
fi
echo ""

# 13. Register another user to test follow
echo -e "${GREEN}13. REGISTER SECOND USER (for follow testing)${NC}"
REGISTER_RESPONSE_2=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "$HEADERS_JSON" \
  -d '{
    "username": "testuser2",
    "email": "testuser2@bennett.edu.in",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "field_of_interest": "sports"
  }')

USER_ID_2=$(echo "$REGISTER_RESPONSE_2" | jq '.user.id')
echo "Second User ID: $USER_ID_2"
echo ""

# 14. Follow User
echo -e "${GREEN}14. FOLLOW USER${NC}"
FOLLOW_RESPONSE=$(curl -s -X POST "$BASE_URL/engagement/follow/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d "{
    \"following\": $USER_ID_2
  }")

echo "$FOLLOW_RESPONSE" | jq .
echo ""

# 15. Get Leaderboard
echo -e "${GREEN}15. GET LEADERBOARD (ACADEMICS, ALL_TIME)${NC}"
curl -s -X GET "$BASE_URL/leaderboard/?field=academics&period=all_time&limit=10" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 16. Get User Rankings
echo -e "${GREEN}16. GET USER RANKINGS${NC}"
curl -s -X GET "$BASE_URL/leaderboard/user/$USER_ID/" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 17. Endorse User Skill
echo -e "${GREEN}17. ENDORSE USER SKILL${NC}"
curl -s -X POST "$BASE_URL/endorsements/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d "{
    \"endorsed_user_id\": $USER_ID_2,
    \"skill\": \"Leadership\"
  }" | jq .
echo ""

# 18. Get User Endorsements
echo -e "${GREEN}18. GET USER ENDORSEMENTS${NC}"
curl -s -X GET "$BASE_URL/endorsements/?user_id=$USER_ID_2" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 19. Get User Followers
echo -e "${GREEN}19. GET USER FOLLOWERS${NC}"
curl -s -X GET "$BASE_URL/users/$USER_ID/followers/" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 20. Get User Following
echo -e "${GREEN}20. GET USER FOLLOWING${NC}"
curl -s -X GET "$BASE_URL/users/$USER_ID/following/" \
  -H "$HEADERS_JSON" | jq .
echo ""

# 21. Unlike Post
echo -e "${GREEN}21. UNLIKE POST${NC}"
if [ ! -z "$LIKE_ID" ] && [ "$LIKE_ID" != "null" ]; then
  curl -s -X DELETE "$BASE_URL/engagement/likes/$LIKE_ID/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "$HEADERS_JSON"
  echo "Unliked successfully"
else
  echo "Like ID not found, skipping"
fi
echo ""

# 22. Delete Comment
echo -e "${GREEN}22. DELETE COMMENT${NC}"
if [ ! -z "$COMMENT_ID" ] && [ "$COMMENT_ID" != "null" ]; then
  curl -s -X DELETE "$BASE_URL/engagement/comments/$COMMENT_ID/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "$HEADERS_JSON"
  echo "Deleted successfully"
else
  echo "Comment ID not found, skipping"
fi
echo ""

# 23. Update Post
echo -e "${GREEN}23. UPDATE POST${NC}"
curl -s -X PUT "$BASE_URL/posts/$POST_ID/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" \
  -d '{
    "title": "Got A* in Database - Updated!",
    "description": "Studied hard for 3 months. Finally got the grade! Feeling proud!"
  }' | jq .
echo ""

# 24. Delete Post
echo -e "${GREEN}24. DELETE POST${NC}"
curl -s -X DELETE "$BASE_URL/posts/$POST_ID/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON"
echo "Post deleted successfully"
echo ""

# 25. Unfollow User
echo -e "${GREEN}25. UNFOLLOW USER${NC}"
curl -s -X DELETE "$BASE_URL/engagement/unfollow/$USER_ID_2/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "$HEADERS_JSON" | jq .
echo ""

echo -e "${GREEN}=== Testing Complete ===${NC}"
