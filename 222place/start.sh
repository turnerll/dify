#!/bin/bash
# 222.place Quick Start Script

set -e

echo "🚀 Starting 222.place Social Matching Application"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Prerequisites check passed"

# Navigate to 222place directory
cd "$(dirname "$0")"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success "Environment file created"
else
    print_status "Environment file already exists"
fi

# Create necessary directories
mkdir -p logs uploads

# Stop any existing containers
print_status "Stopping any existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true

# Build and start services
print_status "Building and starting services..."
docker-compose up --build -d

# Wait for database to be ready
print_status "Waiting for database to be ready..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U postgres -d place222 2>/dev/null; then
        print_success "Database is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Database failed to start within timeout"
        exit 1
    fi
    sleep 2
done

# Wait for API to be ready
print_status "Waiting for API to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:5001/health &>/dev/null; then
        print_success "API is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "API failed to start within timeout"
        exit 1
    fi
    sleep 2
done

# Initialize database with seed data
print_status "Initializing database with seed data..."
if python3 scripts/init_db.py; then
    print_success "Database initialized with seed data"
else
    print_warning "Failed to initialize database - continuing anyway"
fi

# Run smoke tests
print_status "Running smoke tests..."
if python3 scripts/smoke_test.py; then
    print_success "All smoke tests passed!"
else
    print_warning "Some smoke tests failed - check the logs"
fi

# Display status
print_status "Checking service status..."
docker-compose ps

echo ""
echo "🎉 222.place is now running!"
echo "============================="
echo ""
echo "🌐 Web Interface: http://localhost"
echo "🔧 API Endpoint:  http://localhost:5001"
echo "📊 Health Check:  http://localhost/health"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop:      docker-compose down"
echo "🔄 To restart:   docker-compose restart"
echo ""
echo "🧪 Test the application:"
echo "  1. Open http://localhost in your browser"
echo "  2. Complete the onboarding form"
echo "  3. Check your matches and events"
echo ""

# Optional: Open browser (if available)
if command -v xdg-open &> /dev/null; then
    print_status "Opening application in browser..."
    xdg-open http://localhost &>/dev/null || true
elif command -v open &> /dev/null; then
    print_status "Opening application in browser..."
    open http://localhost &>/dev/null || true
fi

print_success "Setup complete! Happy matching! 🎯"