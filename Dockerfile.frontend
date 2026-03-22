FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend_package.json package.json
COPY frontend_package.json.lock package-lock.json

# Install dependencies
RUN npm ci

# Copy source
COPY frontend_App.tsx src/App.tsx
COPY frontend_DashboardPage.tsx src/pages/DashboardPage.tsx
COPY frontend_AgentControlPanel.tsx src/components/AgentControlPanel.tsx

# Build
RUN npm run build

# Production image
FROM node:18-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built app
COPY --from=builder /app/build build

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Expose port
EXPOSE 3000

# Run
CMD ["serve", "-s", "build", "-l", "3000"]
