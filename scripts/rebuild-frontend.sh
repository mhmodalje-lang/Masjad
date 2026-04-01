#!/bin/bash
# Rebuild frontend and restart
echo "🔨 Building frontend..."
cd /app/frontend && yarn build 2>&1 | tail -5
echo "🔄 Restarting frontend server..."
sudo supervisorctl restart frontend
sleep 5
echo "✅ Frontend rebuilt and restarted!"
sudo supervisorctl status frontend
