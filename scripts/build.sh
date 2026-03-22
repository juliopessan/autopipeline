#!/bin/bash
set -e

echo "🔨 Building Vite Frontend..."
cd apps/frontend
npm ci
npm run build
cd ../..

echo "✅ Build completo!"
echo "Frontend: apps/frontend/dist"
