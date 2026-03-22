# 🚀 Azure Autonomous Data Platform - Setup & Deployment Guide

## Table of Contents

1. [Quick Start (Local)](#quick-start-local)
2. [Development Setup](#development-setup)
3. [Azure Configuration](#azure-configuration)
4. [Deployment to Azure](#deployment-to-azure)
5. [Docker Deployment](#docker-deployment)
6. [Environment Variables](#environment-variables)
7. [API Endpoints Reference](#api-endpoints-reference)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start (Local)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- ANTHROPIC_API_KEY (from Claude)

### 1️⃣ Clone & Setup Backend

```bash
# Clone repository
git clone https://github.com/fcamara/autopipeline.git
cd autopipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend_requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run backend
python backend_main.py
```

Backend will run on: **http://localhost:8000**

### 2️⃣ Setup Frontend

```bash
# In another terminal
cd frontend

# Install dependencies
npm install

# Run frontend
npm start
```

Frontend will run on: **http://localhost:3000**

### 3️⃣ Verify Setup

```bash
# Check backend health
curl http://localhost:8000/health

# Check Azure connection
curl http://localhost:8000/api/azure-status

# Open browser
open http://localhost:3000
```

---

## Development Setup

### Full Setup with Docker Compose

```bash
# 1. Create .env from example
cp .env.example .env

# 2. Edit .env with your credentials
nano .env

# 3. Build and run containers
docker-compose up -d

# 4. Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# 5. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Development Commands

```bash
# Stop containers
docker-compose down

# Rebuild containers
docker-compose up --build

# Run tests
docker-compose exec backend pytest

# Database migrations (if using PostgreSQL)
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs backend -f
docker-compose logs frontend -f

# Shell access
docker-compose exec backend python
docker-compose exec frontend sh
```

---

## Azure Configuration

### 1️⃣ Set Up Service Principal

```bash
# Create service principal
az ad sp create-for-rbac --name autopipeline-sp --role Contributor

# Save the output - you'll need:
# - clientId (AZURE_CLIENT_ID)
# - clientSecret (AZURE_CLIENT_SECRET)
# - tenantId (AZURE_TENANT_ID)
```

### 2️⃣ Provision Azure Resources

```bash
# Set variables
export RG_NAME="rg-autopipeline"
export LOCATION="eastus2"

# Create resource group
az group create --name $RG_NAME --location $LOCATION

# Deploy Terraform (from quick-start-guide.md)
cd terraform
terraform init
terraform plan
terraform apply
```

### 3️⃣ Configure Permissions

```bash
# Grant Synapse permissions
az role assignment create \
  --assignee <client-id> \
  --role "SQL Administrator" \
  --scope /subscriptions/<subscription-id>/resourceGroups/$RG_NAME

# Grant Storage permissions
az role assignment create \
  --assignee <client-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<subscription-id>/resourceGroups/$RG_NAME

# Grant Cost Management permissions
az role assignment create \
  --assignee <client-id> \
  --role "Cost Management Contributor" \
  --scope /subscriptions/<subscription-id>
```

---

## Deployment to Azure

### Option 1: Azure Container Instances (Recommended for MVP)

```bash
# Set variables
export ACR_NAME="yourregistry"
export ACR_LOGIN_SERVER="$ACR_NAME.azurecr.io"

# Build and push images
docker build -f Dockerfile.backend -t $ACR_LOGIN_SERVER/autopipeline-backend:latest .
docker build -f Dockerfile.frontend -t $ACR_LOGIN_SERVER/autopipeline-frontend:latest .

docker push $ACR_LOGIN_SERVER/autopipeline-backend:latest
docker push $ACR_LOGIN_SERVER/autopipeline-frontend:latest

# Deploy to ACI
az container create \
  --resource-group $RG_NAME \
  --name autopipeline-backend \
  --image $ACR_LOGIN_SERVER/autopipeline-backend:latest \
  --ports 8000 \
  --environment-variables \
    ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID \
  --assign-identity \
  --registry-login-server $ACR_LOGIN_SERVER

az container create \
  --resource-group $RG_NAME \
  --name autopipeline-frontend \
  --image $ACR_LOGIN_SERVER/autopipeline-frontend:latest \
  --ports 3000
```

### Option 2: Azure App Service (Production)

```bash
# Create App Service Plan
az appservice plan create \
  --name autopipeline-plan \
  --resource-group $RG_NAME \
  --sku B2 \
  --is-linux

# Deploy backend
az webapp create \
  --resource-group $RG_NAME \
  --plan autopipeline-plan \
  --name autopipeline-backend \
  --deployment-container-image-name $ACR_LOGIN_SERVER/autopipeline-backend:latest

# Deploy frontend
az webapp create \
  --resource-group $RG_NAME \
  --plan autopipeline-plan \
  --name autopipeline-frontend \
  --deployment-container-image-name $ACR_LOGIN_SERVER/autopipeline-frontend:latest

# Configure environment variables
az webapp config appsettings set \
  --resource-group $RG_NAME \
  --name autopipeline-backend \
  --settings ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
```

### Option 3: Azure Kubernetes Service (AKS) (Scale)

```bash
# Create AKS cluster
az aks create \
  --resource-group $RG_NAME \
  --name autopipeline-aks \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard \
  --enable-managed-identity

# Get credentials
az aks get-credentials \
  --resource-group $RG_NAME \
  --name autopipeline-aks

# Apply Kubernetes manifests
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get svc
```

---

## Docker Deployment

### Build Images

```bash
# Backend
docker build -f Dockerfile.backend -t autopipeline-backend:latest .

# Frontend
docker build -f Dockerfile.frontend -t autopipeline-frontend:latest .

# Tag for registry
docker tag autopipeline-backend:latest myregistry.azurecr.io/autopipeline-backend:latest
docker tag autopipeline-frontend:latest myregistry.azurecr.io/autopipeline-frontend:latest

# Push to registry
docker push myregistry.azurecr.io/autopipeline-backend:latest
docker push myregistry.azurecr.io/autopipeline-frontend:latest
```

### Run Locally with Docker Compose

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
```

---

## Environment Variables

### Required (Always)

```bash
ANTHROPIC_API_KEY=sk-...          # Claude API key
AZURE_SUBSCRIPTION_ID=xxx-xxx-xxx # Azure subscription
AZURE_RESOURCE_GROUP=rg-autopipeline
```

### Optional (With Real Azure)

```bash
AZURE_TENANT_ID=xxx-xxx-xxx
AZURE_CLIENT_ID=xxx-xxx-xxx
AZURE_CLIENT_SECRET=xxx-xxx-xxx
SYNAPSE_SERVER=syn-yourname.sql.azuresynapse.net
SYNAPSE_DATABASE=analytics
STORAGE_ACCOUNT=stautopipelineprod
APPINSIGHTS_KEY=xxx-xxx-xxx
```

### Application Settings

```bash
ENVIRONMENT=development  # development, staging, production
LOG_LEVEL=INFO
DEBUG=false
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Agent Configuration

```bash
AGENT_TIME_BUDGET_SECONDS=600
AGENT_COST_LIMIT_USD=5.0
AGENT_MAX_ITERATIONS=100
AGENT_ENABLED=true
```

---

## API Endpoints Reference

### Health & Status

```bash
GET /health
GET /api/azure-status
```

### Programs

```bash
GET /api/programs                    # List all programs
POST /api/programs                   # Create program
GET /api/programs/{program_id}       # Get program details
GET /api/programs/{program_id}/metrics  # Get metrics
```

### Experiments

```bash
POST /api/experiments                # Run experiment
GET /api/experiments                 # List experiments
GET /api/experiments/{experiment_id} # Get details
```

### Agent

```bash
POST /api/agent/propose              # Get Claude proposal
POST /api/agent/start-loop           # Start autonomous loop
POST /api/agent/stop-loop            # Stop autonomous loop
```

### Dashboard

```bash
GET /api/dashboard                   # Get all dashboard data
```

### Full API Documentation

```
http://localhost:8000/docs           # Swagger UI
http://localhost:8000/redoc          # ReDoc
```

---

## Troubleshooting

### Backend Issues

**Problem:** `ANTHROPIC_API_KEY not set`
```bash
export ANTHROPIC_API_KEY=sk-your-key
# Or add to .env file
```

**Problem:** `Port 8000 already in use`
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
python backend_main.py --port 8001
```

**Problem:** `ModuleNotFoundError`
```bash
pip install --upgrade -r backend_requirements.txt
```

### Frontend Issues

**Problem:** `npm ERR! ERESOLVE unable to resolve dependency`
```bash
npm install --legacy-peer-deps
```

**Problem:** Frontend can't reach backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check REACT_APP_API_URL environment variable
echo $REACT_APP_API_URL

# Set if needed
export REACT_APP_API_URL=http://localhost:8000
```

**Problem:** Port 3000 in use
```bash
PORT=3001 npm start
```

### Azure Connection Issues

**Problem:** `Azure credentials not configured`
```bash
# Check if running in mock mode (expected for demo)
curl http://localhost:8000/api/azure-status
# Should show: "mock": true

# To use real Azure:
export AZURE_SUBSCRIPTION_ID=your-id
export AZURE_CLIENT_ID=your-id
# etc...
```

**Problem:** `Synapse query failed`
```bash
# Verify connection string
az sql server show --resource-group $RG --name <server-name>

# Test connectivity
pyodbc tests/test_synapse_connection.py
```

### Docker Issues

**Problem:** `docker-compose: command not found`
```bash
# Install docker-compose
pip install docker-compose
# Or use docker compose (newer versions)
docker compose up -d
```

**Problem:** Containers won't start
```bash
docker-compose logs
docker-compose down -v  # Remove volumes
docker-compose up --build
```

---

## Production Checklist

Before deploying to production:

- [ ] All .env values configured
- [ ] ANTHROPIC_API_KEY set (from https://console.anthropic.com)
- [ ] Azure service principal created
- [ ] Azure resources provisioned (Synapse, ADLS, Insights)
- [ ] CORS origins configured correctly
- [ ] Database created (if using PostgreSQL)
- [ ] Monitoring & alerts set up
- [ ] Backup strategy in place
- [ ] Load balancing configured
- [ ] SSL/TLS certificates installed
- [ ] Security groups / Network policies configured
- [ ] Logs aggregated (Application Insights / Log Analytics)
- [ ] Cost tracking enabled
- [ ] Documentation updated

---

## Support

For issues, check:

1. **Backend logs:** `docker-compose logs backend`
2. **Frontend logs:** `docker-compose logs frontend`
3. **API docs:** http://localhost:8000/docs
4. **GitHub Issues:** https://github.com/fcamara/autopipeline/issues

---

**Ready to deploy? Start with Quick Start (Local) above, then move to Docker, then Azure!** 🚀
