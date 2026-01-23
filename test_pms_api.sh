#!/bin/bash

# PMS API Testing Script
# This script tests all PMS API endpoints to verify the backend is working correctly

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${1:-http://localhost:8000/api}"
USERNAME="${2:-admin}"
PASSWORD="${3:-admin}"

echo "================================================"
echo "PMS API Testing Script"
echo "================================================"
echo "Base URL: $BASE_URL"
echo "Username: $USERNAME"
echo ""

# Step 1: Login and get token
echo -e "${YELLOW}[1] Authenticating...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USERNAME\",
    \"password\": \"$PASSWORD\"
  }")

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
  echo -e "${RED}✗ Authentication failed${NC}"
  echo "Response: $LOGIN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Authentication successful${NC}"
echo "Token: ${ACCESS_TOKEN:0:20}..."
echo ""

# Helper function to test endpoints
test_endpoint() {
  local method=$1
  local endpoint=$2
  local data=$3
  local description=$4

  echo -e "${YELLOW}Testing: $description${NC}"

  if [ "$method" == "GET" ]; then
    RESPONSE=$(curl -s -X GET "$BASE_URL$endpoint" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json")
  elif [ "$method" == "POST" ]; then
    RESPONSE=$(curl -s -X POST "$BASE_URL$endpoint" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$data")
  fi

  if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${RED}✗ Failed${NC}"
    echo "Response: $RESPONSE"
  else
    echo -e "${GREEN}✓ Success${NC}"
    # Pretty print the response (first 100 chars)
    echo "Response: ${RESPONSE:0:100}..."
  fi
  echo ""
}

# Step 2: Test Objectives endpoints
echo -e "${YELLOW}=== OBJECTIVES ===${NC}"
test_endpoint "GET" "/pms/objectives/" "" "List Objectives"

# Step 3: Test Employee Objectives
echo -e "${YELLOW}=== EMPLOYEE OBJECTIVES ===${NC}"
test_endpoint "GET" "/pms/employee-objectives/" "" "List Employee Objectives"

# Step 4: Test Feedback endpoints
echo -e "${YELLOW}=== FEEDBACK ===${NC}"
test_endpoint "GET" "/pms/feedback/" "" "List Feedback Cycles"

# Step 5: Test Meetings endpoints
echo -e "${YELLOW}=== MEETINGS ===${NC}"
test_endpoint "GET" "/pms/meetings/" "" "List Meetings"

# Step 6: Test Bonus Points endpoints
echo -e "${YELLOW}=== BONUS POINTS ===${NC}"
test_endpoint "GET" "/pms/bonus-settings/" "" "List Bonus Settings"
test_endpoint "GET" "/pms/employee-bonus-points/" "" "List Employee Bonus Points"

# Step 7: Test Dashboard
echo -e "${YELLOW}=== DASHBOARD ===${NC}"
test_endpoint "GET" "/pms/dashboard/stats/" "" "Get Dashboard Stats"

# Step 8: Test creating an objective
echo -e "${YELLOW}=== CREATE OBJECTIVE TEST ===${NC}"
OBJECTIVE_DATA='{
  "title": "Test Objective",
  "description": "Test objective created by script",
  "status": "Not Started",
  "duration": 3,
  "duration_unit": "months",
  "manager_ids": [1]
}'
test_endpoint "POST" "/pms/objectives/" "$OBJECTIVE_DATA" "Create Objective"

echo "================================================"
echo "API Testing Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Start the frontend: cd horilla-frontend && npm run dev"
echo "2. Open http://localhost:3000 in your browser"
echo "3. Login with credentials: $USERNAME / $PASSWORD"
echo ""
