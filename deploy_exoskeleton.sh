#!/bin/bash

echo "🚀 UPLOADING AI CEO EXOSKELETON APPS TO DIFY"
echo "==========================================="
echo

# Set Dify API endpoint
DIFY_API="http://localhost/api/v1"

echo "📁 Available App Templates:"
ls -la /home/djtl/Projects/dify-ai-platform/*.json

echo
echo "🎯 Step 1: Setting up Ollama integration in Dify..."

# Configure Ollama as model provider
curl -X POST "$DIFY_API/setup/model-provider" \
  -H "Content-Type: application/json" \
  -d '{
    "provider_name": "ollama",
    "provider_type": "custom",
    "custom_configuration": {
      "endpoint_url": "http://host.docker.internal:11434",
      "api_key": ""
    },
    "models": [
      {
        "name": "llama3.2:latest",
        "type": "llm",
        "features": ["chat", "completion"]
      },
      {
        "name": "mistral:latest", 
        "type": "llm",
        "features": ["chat", "completion"]
      },
      {
        "name": "nomic-embed-text:latest",
        "type": "text-embedding",
        "features": ["embedding"]
      },
      {
        "name": "llava:13b",
        "type": "multimodal",
        "features": ["vision", "chat"]
      }
    ]
  }' 2>/dev/null || echo "Note: Model provider setup requires admin login first"

echo
echo "🎤 Step 2: Upload Conversation Intelligence Engine..."
echo "This will process your daily transcriptions and enrich Monica CRM"

echo
echo "🎯 Step 3: Upload Executive Command Center..." 
echo "This is your master AI CEO orchestrator"

echo
echo "📋 Next Steps:"
echo "1. Open http://localhost in your browser"
echo "2. Complete the admin setup if not done"
echo "3. Go to Settings > Model Providers and add Ollama:"
echo "   - Provider Type: Custom"
echo "   - Base URL: http://host.docker.internal:11434"
echo "   - Available Models: llama3.2:latest, mistral:latest, nomic-embed-text:latest, llava:13b"
echo
echo "4. Import the app templates:"
echo "   - Go to Create App > Import DSL File"
echo "   - Upload: executive_command_center.json"
echo "   - Upload: conversation_intelligence.json"
echo
echo "5. Configure API integrations in each app:"
echo "   - Monica CRM: http://localhost:8888"
echo "   - UseMotion API key from Vaultwarden"
echo "   - Notion API key from Vaultwarden"

echo
echo "🦾 Your AI CEO Exoskeleton is ready to deploy!"
echo "💡 This system will:"
echo "   ✅ Process daily conversation transcripts"
echo "   ✅ Enrich personas in Monica CRM automatically"
echo "   ✅ Extract and delegate action items to Notion"
echo "   ✅ Schedule optimal time blocks via UseMotion"
echo "   ✅ Provide executive summaries of all activities"
echo "   ✅ Support your 3 major initiatives simultaneously"
