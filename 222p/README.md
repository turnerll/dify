# 222.place - Self-Hosted Matchmaking Platform

A privacy-first, open-source matchmaking platform built on top of Dify that connects people through shared interests, activities, and local events.

## Features

- **Comprehensive Onboarding**: 50-80 question assessment covering interests, availability, location, budget, dietary preferences, accessibility needs, and cultural preferences
- **Smart Matching**: Weighted scoring algorithm with optional embedding-based similarity matching
- **Event Suggestions**: AI-powered recommendations for dinners, small gatherings, and group outings
- **Bilingual Support**: English and Spanish friendly UX
- **Privacy-First**: Local deployment with data sovereignty and user consent controls
- **Moderation**: Built-in content filtering and abuse reporting

## Quick Start

### Prerequisites

- Docker and Docker Compose
- 4GB+ RAM recommended
- Git, Node.js, Python 3.8+

### Setup

1. **Clone and setup environment**:
   ```bash
   git clone <repo-url>
   cd dify/222p
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the services**:
   ```bash
   make up
   ```

3. **Initialize the database and seed data**:
   ```bash
   make seed
   ```

4. **Access the application**:
   - Web app: https://localhost:3000
   - API: https://localhost:5000
   - Admin panel: https://localhost:3000/admin

### Testing

Run the smoke test to verify everything is working:
```bash
make test
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │   API Gateway   │    │   Matching API  │
│   (Next.js)     │◄──►│   (Traefik)     │◄──►│   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         │              │   PostgreSQL    │◄────────────┘
         │              │   (Primary DB)  │
         │              └─────────────────┘
         │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Redis       │    │   Celery        │    │    Qdrant       │
│   (Cache/Queue) │◄──►│   (Workers)     │    │  (Vector DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Database Schema

### Core Tables
- `users` - User accounts and authentication
- `profiles` - Extended user profiles with preferences
- `onboarding_responses` - Questionnaire responses
- `matches` - Generated user matches with scores
- `events` - Suggested and user-created events
- `event_invitations` - Event invitations and RSVPs
- `groups` - User groups and communities
- `messages` - In-app messaging
- `moderation_flags` - Content moderation reports

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

### Onboarding
- `GET /onboarding/questions` - Get questionnaire
- `POST /onboarding/responses` - Submit responses

### Matching
- `POST /matches/generate` - Generate matches for user
- `GET /matches` - Get user's matches

### Events
- `GET /events/suggestions` - Get event suggestions
- `POST /events` - Create new event
- `POST /events/{id}/invite` - Send invitation

### Social
- `POST /groups` - Create group
- `POST /messages` - Send message
- `POST /moderation/report` - Report content

## Commands

- `make up` - Start all services
- `make down` - Stop all services
- `make logs` - View logs
- `make seed` - Seed database with sample data
- `make test` - Run smoke tests
- `make clean` - Clean up containers and volumes
- `make backup` - Backup database
- `make restore` - Restore database

## Environment Variables

See `.env.example` for full configuration options.

Key variables:
- `SECRET_KEY` - Application secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SMTP_*` - Email configuration
- `CORS_ORIGINS` - Allowed CORS origins

## Security

- All API endpoints require authentication
- HTTPS enforced in production
- Rate limiting on sensitive endpoints
- Input validation and sanitization
- Content moderation for user-generated content
- Audit logging for sensitive operations

## Privacy

- Minimal data collection
- User consent for all features
- Data retention policies
- GDPR-compliant data export/deletion
- Local deployment option for full data sovereignty

## Development

### Backend Development
```bash
cd api
uv run --project . python app.py
```

### Frontend Development
```bash
cd web
pnpm dev
```

### Running Tests
```bash
make test-unit
make test-integration
make test-e2e
```

## Deployment

### Production Deployment
1. Update production environment variables
2. Set up SSL certificates
3. Configure external database if needed
4. Set up monitoring and logging
5. Configure backup strategy

### Scaling
- Multiple API instances behind load balancer
- Separate read replicas for database
- Redis cluster for high availability
- CDN for static assets

## Support

- Documentation: [Link to docs]
- Issues: [Link to issue tracker]
- Community: [Link to community forum]

## License

MIT License - see LICENSE file for details.