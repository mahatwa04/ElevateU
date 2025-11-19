#!/bin/bash

# Start Backend Server
echo "🚀 Starting Backend Server on port 8000..."
cd /Users/mahatwasharma/Desktop/ElevateU/Backend
source venv/bin/activate
python manage.py runserver 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started with PID: $BACKEND_PID"

# Wait a moment for backend to start
sleep 3

# Start Frontend Server
echo "🚀 Starting Frontend Server on port 5173..."
cd /Users/mahatwasharma/Desktop/ElevateU/Frontend
source ~/.nvm/nvm.sh
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started with PID: $FRONTEND_PID"

# Wait a moment for frontend to start
sleep 4

# Check if servers are running
echo ""
echo "📋 Checking server status..."
echo ""

curl -s http://localhost:8000/api/health/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend API: http://localhost:8000/api/health/ - RUNNING"
else
    echo "❌ Backend API: NOT RESPONDING"
fi

curl -s http://localhost:5173/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend: http://localhost:5173/ - RUNNING"
else
    echo "❌ Frontend: NOT RESPONDING"
fi

echo ""
echo "════════════════════════════════════════════════════"
echo "🌐 WEBSITE: http://localhost:5173"
echo "🔧 BACKEND: http://localhost:8000/api/"
echo "⚙️  ADMIN: http://localhost:8000/admin"
echo "════════════════════════════════════════════════════"
echo ""
echo "Logs:"
echo "  Backend: tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""
echo "To stop servers: kill $BACKEND_PID $FRONTEND_PID"
echo ""
