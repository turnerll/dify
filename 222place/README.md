# 222.place - Social Matching Application

A social matching platform built on top of Dify that connects people through shared interests, availability, and preferences for dinners, gatherings, and group activities.

## Architecture

This application extends the Dify platform with:
- **Backend**: Python Flask API with 222.place-specific endpoints
- **Frontend**: Next.js React application with bilingual support
- **Database**: PostgreSQL with additional tables for social matching
- **Infrastructure**: Docker Compose with Redis, vector store, and reverse proxy

## Features

### Core Functionality
- 50-80 question onboarding process (English/Spanish)
- AI-powered matching algorithm with fairness controls
- Event suggestions for dinners, gatherings, and group outings
- Real-time messaging and group coordination
- Content moderation and abuse reporting

### Matching Criteria
- Interests and hobbies compatibility
- Geographic proximity and location preferences
- Schedule availability alignment
- Budget range compatibility
- Dietary restrictions and preferences
- Cultural and language preferences
- Transportation needs and accessibility

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd dify

# Start the complete stack
cp docker/.env.example docker/.env
# Edit docker/.env with your configuration
docker-compose up -d

# Run seed data
docker exec -it dify-api-1 python /app/scripts/seed_222place.py

# Access the application
open http://localhost
```

## Development

See [Development Guide](./DEVELOPMENT.md) for detailed setup instructions.

## Security & Privacy

- HTTPS encryption for all communications
- Content moderation filters
- User abuse reporting system
- Privacy-by-design data handling
- Rate limiting and audit logging