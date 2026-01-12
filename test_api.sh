#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Testing Sustainable Shine Backend API${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Get bookings
echo -e "${GREEN}Test 1: GET /api/bookings/${NC}"
curl -s http://localhost:8000/api/bookings/ | python3 -m json.tool
echo ""
echo ""

# Test 2: Get blog posts
echo -e "${GREEN}Test 2: GET /api/blog/${NC}"
curl -s http://localhost:8000/api/blog/ | python3 -m json.tool
echo ""
echo ""

# Test 3: Get statistics
echo -e "${GREEN}Test 3: GET /api/bookings/statistics/${NC}"
curl -s http://localhost:8000/api/bookings/statistics/ | python3 -m json.tool
echo ""
echo ""

# Test 4: Get featured blog posts
echo -e "${GREEN}Test 4: GET /api/blog/featured/${NC}"
curl -s http://localhost:8000/api/blog/featured/ | python3 -m json.tool
echo ""
echo ""

# Test 5: Create a test booking
echo -e "${GREEN}Test 5: POST /api/bookings/ (Create test booking)${NC}"
curl -s -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "serviceType": "general",
    "frequency": "once",
    "bedrooms": 3,
    "bathrooms": 2,
    "kitchen": 1,
    "livingDining": 1,
    "laundry": 1,
    "storey": 1,
    "selectedAddOns": {},
    "addOnDetails": {},
    "selectedDate": "2026-01-20",
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "phone": "0412345678",
    "smsReminders": true,
    "street": "123 Test Street",
    "suburb": "Sydney",
    "postcode": "2000",
    "priceDetails": {
      "total": 158,
      "subtotal": 143.64,
      "gst": 14.36
    }
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}API Testing Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
