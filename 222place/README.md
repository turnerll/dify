# 222.place - Social Matching Application

A sophisticated social matching platform that connects people through shared interests, availability, and preferences for dinners, gatherings, and group activities. Built on modern web technologies with AI-powered matching algorithms.

## 🌟 Features

### Core Functionality
- **Comprehensive Onboarding**: 52 bilingual questions covering interests, availability, budget, and preferences
- **Smart Matching Algorithm**: Geographic proximity, interest compatibility, and preference alignment
- **Event System**: Dinners, small gatherings, and group outings (concerts, sports events)
- **Real-time Communication**: Messaging system for matches and groups
- **Safety First**: Content moderation, abuse reporting, and privacy controls

### Multilingual Support
- **English and Spanish** throughout the entire application
- Seamless language switching
- Culturally appropriate content and examples

### Matching Criteria
- 🗺️ **Geographic Proximity**: Configurable distance preferences
- 🎯 **Interest Alignment**: Hobbies, activities, and lifestyle preferences  
- 📅 **Schedule Compatibility**: Availability and timing preferences
- 💰 **Budget Range**: Financial comfort zone matching
- 🍽️ **Dietary Preferences**: Food restrictions and cuisine preferences
- 🌍 **Cultural Affinity**: Language and cultural background preferences
- ♿ **Accessibility**: Transportation and accessibility needs

## 🚀 Quick Start

### Option 1: One-Command Setup
```bash
cd 222place
./start.sh
```

### Option 2: Manual Setup
```bash
# 1. Setup environment
cd 222place
cp .env.example .env

# 2. Start services
docker-compose up --build -d

# 3. Initialize database
python3 scripts/init_db.py

# 4. Run tests
python3 scripts/smoke_test.py
```

### Access the Application
- **Web Interface**: http://localhost
- **API Docs**: http://localhost:5001/health
- **Database**: PostgreSQL on localhost:5432

## 🏗️ Architecture

### Backend (API)
- **Framework**: Flask with RESTful API design
- **Database**: PostgreSQL with optimized indexes
- **Cache**: Redis for sessions and caching
- **Security**: JWT authentication, input validation, rate limiting

### Frontend (Web)
- **Technology**: Modern HTML5/CSS3/JavaScript
- **Design**: Responsive, mobile-first approach
- **Accessibility**: WCAG compliant, screen reader friendly
- **Internationalization**: Built-in English/Spanish support

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **Reverse Proxy**: Nginx with CORS handling
- **Monitoring**: Health checks and logging
- **Scalability**: Microservices-ready architecture

## 📊 Database Schema

### Core Tables
- `social_questions` - Bilingual onboarding questions
- `social_profiles` - Extended user profiles with location data
- `social_responses` - User answers to questions
- `social_matches` - Calculated compatibility scores
- `social_events` - Events and activities
- `social_invitations` - Event RSVPs and invitations
- `social_groups` - Social groups and communities
- `social_messages` - Communication system
- `social_moderation_flags` - Safety and abuse reporting

## 🎯 Matching Algorithm

### Compatibility Scoring
1. **Location Distance**: Haversine formula for geographic proximity
2. **Interest Overlap**: Jaccard similarity for shared interests
3. **Preference Alignment**: Weighted scoring for lifestyle preferences
4. **Schedule Compatibility**: Time availability matching
5. **Budget Alignment**: Financial comfort zone overlap

### Fairness Controls
- **Diversity Filters**: Prevents homogenous clustering
- **Balanced Recommendations**: Ensures varied match suggestions
- **Bias Mitigation**: Algorithmic fairness checks

## 🛠️ Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Development Commands
```bash
# Start development environment
docker-compose up --build

# View logs
docker-compose logs -f

# Run database migrations
python3 scripts/init_db.py

# Run tests
python3 scripts/smoke_test.py

# Access database console
docker-compose exec db psql -U postgres -d place222

# Stop services
docker-compose down
```

### API Endpoints
```
GET  /health                              # Health check
GET  /v1/social/onboarding/questions      # Get questions
POST /v1/social/onboarding/responses      # Submit responses
POST /v1/social/matching                  # Generate matches
GET  /v1/social/matching                  # Get matches
GET  /v1/social/events                    # Get events
```

## 🔒 Security & Privacy

### Security Measures
- **HTTPS**: SSL/TLS encryption (configure certificates)
- **Authentication**: JWT-based secure authentication
- **Input Validation**: Comprehensive data sanitization
- **Rate Limiting**: Protection against abuse
- **SQL Injection Protection**: Parameterized queries

### Privacy Controls
- **Data Minimization**: Only necessary data collection
- **User Consent**: Explicit consent for data processing
- **Right to Delete**: User data removal capabilities
- **Audit Logging**: Track data access and modifications

### Content Moderation
- **Automated Filtering**: Basic content moderation
- **User Reporting**: Abuse reporting system
- **Moderator Tools**: Review and action capabilities

## 🧪 Testing

### Smoke Tests
The application includes comprehensive smoke tests:
```bash
python3 scripts/smoke_test.py
```

### Test Coverage
- ✅ API endpoint functionality
- ✅ Database connectivity
- ✅ Authentication flow
- ✅ Matching algorithm
- ✅ Form submission
- ✅ Error handling

## 🌍 Deployment

### Production Checklist
- [ ] Update environment variables in `.env`
- [ ] Configure SSL certificates
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Performance testing
- [ ] Security audit

### Environment Variables
Key variables to configure:
```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
DB_PASSWORD=your-secure-password
REDIS_PASSWORD=your-redis-password
DEBUG=false  # For production
```

## 📈 Monitoring

### Health Checks
- **Application**: http://localhost/health
- **Database**: Connection and query health
- **Redis**: Cache connectivity

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f api
docker-compose logs -f db
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code Style
- Python: Follow PEP 8
- JavaScript: ES6+ standards
- HTML/CSS: Semantic markup

## 📋 Roadmap

### Phase 1 (Current) ✅
- Core matching functionality
- Basic event system
- Bilingual support
- Database schema

### Phase 2 (Next)
- [ ] Mobile app (React Native)
- [ ] Advanced matching with ML
- [ ] Real-time chat
- [ ] Push notifications

### Phase 3 (Future)
- [ ] Video calling integration
- [ ] AI-powered event suggestions
- [ ] Social proof and reviews
- [ ] Integration with calendar apps

## 🆘 Troubleshooting

### Common Issues

**Database connection failed:**
```bash
# Check if database is running
docker-compose ps db

# Restart database
docker-compose restart db
```

**API not responding:**
```bash
# Check API logs
docker-compose logs api

# Restart API
docker-compose restart api
```

**Port conflicts:**
```bash
# Check what's using the port
sudo lsof -i :80
sudo lsof -i :5001

# Stop conflicting services or change ports in docker-compose.yaml
```

### Support
- Check logs: `docker-compose logs -f`
- Run health checks: `curl http://localhost/health`
- Verify database: `docker-compose exec db psql -U postgres -d place222`

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built on the foundation of the Dify platform
- Inspired by 222.place for social connection
- Community feedback and contributions

---

**Ready to connect people and build communities? Let's make meaningful connections happen! 🎯**