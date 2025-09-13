#!/bin/bash
# Direct AI CEO Import using curl

DIFY_URL="http://localhost"
ADMIN_EMAIL="djtlmed@gmail.com" 
ADMIN_PASSWORD="Infinity00di!"
AI_CEO_FILE="/home/djtl/Projects/dify-ai-platform/ai_ceo_assistant_simple.json"

echo "🚀 AUTOMATED AI CEO IMPORT WITH CURL"
echo "===================================="
echo
echo "📧 Email: $ADMIN_EMAIL"
echo "📁 File: $AI_CEO_FILE"
echo

# Step 1: Login to get session token
echo "🔐 Step 1: Logging in..."
LOGIN_RESPONSE=$(curl -s -c cookies.txt -X POST \
  "$DIFY_URL/console/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "✅ Login successful!"
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    echo "🔑 Got access token: ${ACCESS_TOKEN:0:20}..."
else
    echo "❌ Login failed!"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi

# Step 2: Import AI CEO Assistant
echo
echo "🤖 Step 2: Importing AI CEO Assistant..."

IMPORT_RESPONSE=$(curl -s -X POST \
  "$DIFY_URL/console/api/apps/import" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @"$AI_CEO_FILE")

if echo "$IMPORT_RESPONSE" | grep -q '"id"'; then
    echo "🎉 AI CEO Assistant imported successfully!"
    APP_ID=$(echo "$IMPORT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    echo "✅ App ID: $APP_ID"
    echo "🌟 Your AI CEO is now available at: $DIFY_URL/app/$APP_ID"
else
    echo "❌ Import failed!"
    echo "Response: $IMPORT_RESPONSE"
    exit 1
fi

# Cleanup
rm -f cookies.txt

echo
echo "🎉 SUCCESS! Your AI CEO Command Center is ready!"
echo "=" * 50
echo "🌐 Dashboard: $DIFY_URL"
echo "🤖 Your AI CEO Assistant is ready to use!"
echo "💡 Go to Dify and start chatting with your AI CEO!"
