# 🚀 RUN THE FULLSTACK PLATFORM NOW!

## 5-Minute Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- ANTHROPIC_API_KEY (get from https://console.anthropic.com)

---

## OPTION 1: Run Locally (Simplest)

### Terminal 1: Backend
```bash
# Set your Claude API key
export ANTHROPIC_API_KEY=sk-your-actual-key

# Run backend
python backend_main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend
```bash
# Install dependencies (first time only)
cd frontend
npm install

# Start frontend
npm start
```

You should see:
```
webpack compiled successfully
Compiled successfully!
```

### Open Browser
```
http://localhost:3000
```

**That's it! You now have:**
- ✅ Dashboard running (http://localhost:3000)
- ✅ Backend API running (http://localhost:8000)
- ✅ Agent integration ready
- ✅ Azure integration in mock mode (works without credentials)

---

## OPTION 2: Run with Docker Compose (Cleaner)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env (add your ANTHROPIC_API_KEY)
nano .env

# 3. Build and run
docker-compose up --build

# 4. Open browser
open http://localhost:3000
```

Both containers will start, and you can access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## OPTION 3: Deploy to Azure (See Setup Guide)

For Azure Container Instances, App Service, or Kubernetes:
```bash
# Read the complete guide
cat SETUP-DEPLOYMENT-GUIDE.md
```

---

## 🎯 What to Do First (After Starting)

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

### 2. View API Documentation
```
http://localhost:8000/docs
```

### 3. Create a Program
```bash
curl -X POST http://localhost:8000/api/programs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Pipeline Optimization",
    "constraints": "Can optimize SQL queries and aggregation windows",
    "optimization_goal": "Minimize query latency",
    "metric_name": "latency_seconds",
    "baseline_value": 120,
    "target_value": 20,
    "max_iterations": 100
  }'
```

### 4. In Frontend (http://localhost:3000)
- Click "Programs" → View your created program
- Click "Dashboard" → See real-time metrics
- Click "Agent Control" → Start autonomous loop
- Watch agent optimize your pipeline!

---

## 🧪 Quick Test Sequence

```bash
# 1. Check backend is healthy
curl http://localhost:8000/health

# 2. Create a program
PROGRAM_ID=$(curl -s -X POST http://localhost:8000/api/programs \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","constraints":"Test","optimization_goal":"Minimize metric","metric_name":"metric","baseline_value":100,"target_value":50,"max_iterations":10}' | jq -r '.id')

echo "Created program: $PROGRAM_ID"

# 3. Run an experiment
curl -X POST http://localhost:8000/api/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "program_id":"'$PROGRAM_ID'",
    "analysis_code":"def get_metric(): return 95.0",
    "description":"Test experiment"
  }'

# 4. Get proposal from Claude
curl -X POST "http://localhost:8000/api/agent/propose?program_id=$PROGRAM_ID"

# 5. View dashboard
open http://localhost:3000
```

---

## 📊 What You'll See

### Dashboard
- 6 KPI cards (total experiments, success rate, costs, budget)
- Metric trend chart showing improvements
- Cost summary chart
- Recent experiments table
- Active programs grid

### Agent Control
- Start/stop autonomous loop
- Request Claude proposals
- View agent status
- Monitor system health

### Programs
- Create new optimization programs
- View program details
- Track metrics

### Experiments
- View all experiment results
- Filter by program
- Track success rates
- Monitor costs

---

## ⚡ Features Available (No Azure Needed!)

✅ **Claude Integration** - Get AI proposals for improvements  
✅ **Experiment Engine** - Run experiments with budget enforcement  
✅ **Dashboard** - Real-time metrics & KPIs  
✅ **Agent Control** - Start/stop autonomous loop  
✅ **Mock Azure** - Run without Azure credentials (for demo)  

When you add Azure credentials (to .env), you'll also get:
- Real Synapse SQL queries
- Real ADLS Gen2 data loading
- Real Application Insights tracking
- Real cost monitoring

---

## 🔧 Troubleshooting

### Backend won't start?
```bash
pip install -r backend_requirements.txt
python backend_main.py
```

### Frontend won't start?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm start
```

### Port 3000 already in use?
```bash
PORT=3001 npm start
```

### Port 8000 already in use?
```bash
python backend_main.py --host 0.0.0.0 --port 8001
```

### Docker issues?
```bash
docker-compose down -v
docker-compose up --build
```

---

## 📚 Next Steps (After Testing)

1. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Create multiple programs

2. **Test Claude Agent**
   - Click "Agent Control"
   - Get proposals
   - Watch agent optimize

3. **Add Azure Credentials** (Optional)
   - Edit .env with Azure keys
   - Watch real Synapse queries
   - Monitor real costs

4. **Deploy** (See SETUP-DEPLOYMENT-GUIDE.md)
   - Docker Compose → Local dev
   - Azure ACI → Quick prod
   - Azure App Service → Scalable prod
   - Azure AKS → Enterprise

---

## 📖 Documentation

| File | Purpose |
|---|---|
| **FULLSTACK-SUMMARY.md** | Overview of what you have |
| **SETUP-DEPLOYMENT-GUIDE.md** | Complete setup & deployment |
| **backend_main.py** | FastAPI backend (documented) |
| **frontend_App.tsx** | React frontend (documented) |
| **.env.example** | All configuration variables |

---

## ✨ Architecture

```
Your Browser
    ↓
    ├─→ http://localhost:3000 (React Frontend)
    │
    └─→ http://localhost:8000 (FastAPI Backend)
            ↓
            ├─→ Claude API (Proposals)
            ├─→ Synapse (Queries) [Mock/Real]
            ├─→ ADLS Gen2 (Data) [Mock/Real]
            └─→ App Insights (Metrics) [Mock/Real]
```

---

## 🎉 You're Ready!

**Everything is configured and ready to run.**

### Start Now:
```bash
# Backend
python backend_main.py

# Frontend (new terminal)
cd frontend && npm start

# Open http://localhost:3000
```

### That's it! You have a production-ready fullstack platform with:
- Python/FastAPI backend
- React/TypeScript frontend
- Claude agent integration
- Azure service connections
- Real-time dashboard
- Experiment tracking
- Agent control panel

---

**Questions?** Check SETUP-DEPLOYMENT-GUIDE.md or view API docs at http://localhost:8000/docs

**Status:** ✅ Production-Ready  
**Time to Start:** 5 minutes  
**Time to Prod:** Follow setup guide (2-4 hours)  

**LET'S GO! 🚀**
