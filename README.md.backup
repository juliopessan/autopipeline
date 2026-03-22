# 🤖 Azure Autonomous Data Platform

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen?style=flat-square)](https://github.com/juliopessan/autopipeline)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-18%2B-green?style=flat-square)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-24%2B-blue?style=flat-square)](https://www.docker.com/)
[![Azure](https://img.shields.io/badge/azure-cloud-blue?style=flat-square)](https://azure.microsoft.com/)
[![Claude AI](https://img.shields.io/badge/Claude-AI%20Powered-orange?style=flat-square)](https://claude.ai/)

**Production-ready autonomous data pipeline optimization platform powered by Claude AI and Microsoft Azure**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup & Deployment](#setup--deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Azure Autonomous Data Platform** is a production-ready fullstack application that uses Claude AI to autonomously optimize data pipelines running on Microsoft Azure. The platform enables teams to automatically improve pipeline performance while maintaining complete control, transparency, and budget enforcement.

### The Problem

Data pipelines often run inefficiently due to:
- Manual optimization processes
- Lack of continuous improvement
- High operational costs
- Limited visibility into optimization opportunities

### The Solution

This platform provides:
- **Autonomous optimization** via Claude AI
- **Real-time monitoring** with interactive dashboard
- **Budget enforcement** with time & cost limits
- **Complete auditability** with git-tracked experiments
- **Production-ready** deployment options

### How It Works

```
┌─────────────────────────────────────┐
│    Claude Autonomous Agent 🤖       │
│  Proposes → Executes → Tracks       │
│  → Learns → Improves (Continuously) │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  React Dashboard + FastAPI Backend   │
│  Real-time Metrics & Control Panel   │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│    Azure Services                   │
│  Synapse | ADLS | Insights | Cost   │
└─────────────────────────────────────┘
```

**Flow:** Agent proposes improvement → System executes → Metrics tracked → If better, keep; else revert → Next iteration

---

## ✨ Key Features

### 🤖 Autonomous Optimization
- Claude AI proposes improvements automatically
- Execution happens without human approval
- Budget enforcement (time + cost limits)
- Success-based keep/discard logic
- Continuous improvement loop

### 📊 Real-Time Dashboard
- 6 KPI cards (experiments, success rate, costs, budget)
- Interactive metric trend chart
- Cost summary visualization
- Recent experiments table
- Active programs grid
- Auto-refresh interval selector (2s - 30s)

### 💼 Program Management
- Create optimization programs with custom goals
- Define constraints & boundaries
- Set target metrics & baselines
- Track program-specific metrics
- Full CRUD operations

### ⚗️ Experiment Tracking
- Run individual experiments
- Track results in real-time
- Filter by program
- View detailed metrics
- Status monitoring (success, crash, timeout, budget_exceeded)

### 🎮 Agent Control Panel
- Start/stop autonomous loop
- Manual proposal requests
- View Claude proposals
- Agent status monitoring
- System health indicators

### 🔗 Azure Integration
- **Synapse SQL Pool:** Query execution and data processing
- **ADLS Gen2:** Data lake storage and checkpoints
- **Application Insights:** Metrics tracking and monitoring
- **Cost Management API:** Real-time cost tracking
- **Key Vault:** Secure secrets management
- **Mock mode** for local testing without Azure credentials

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- ANTHROPIC_API_KEY (from https://console.anthropic.com)
- Docker (optional)

### Run Locally (5 Minutes)

**Option 1: Python + npm**

```bash
# Clone repository
git clone https://github.com/juliopessan/autopipeline.git
cd autopipeline

# Backend (Terminal 1)
export ANTHROPIC_API_KEY=sk-your-actual-key
python backend_main.py
# Server runs on http://localhost:8000

# Frontend (Terminal 2)
cd frontend
npm install
npm start
# App opens on http://localhost:3000
```

**Option 2: Docker Compose**

```bash
# Create environment file
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run containers
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Option 3: GitHub CLI (Fastest)**

```bash
# Install & authenticate
gh auth login

# Create and deploy
gh repo clone juliopessan/autopipeline
cd autopipeline
docker-compose up
```

### First Steps

1. **Dashboard:** Visit http://localhost:3000 to see real-time metrics
2. **Create Program:** Click "Programs" → Create a test optimization program
3. **Run Experiment:** Go to "Experiments" → Run test experiment
4. **View Results:** Back to Dashboard → See metrics update
5. **Test Agent:** Click "Agent Control" → Get Claude proposals

---

## 🏗️ Architecture

### System Context

```
┌──────────────────────────────────────────────────────┐
│                    Users                             │
│            (Web Browser / Mobile App)                │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼───────────────────────────────┐
│         Frontend (React/TypeScript)                  │
│  Dashboard | Programs | Experiments | Agent Control  │
└──────────────────────┬───────────────────────────────┘
                       │ REST API
┌──────────────────────▼───────────────────────────────┐
│         Backend (FastAPI/Python)                     │
│  • Claude Agent (Autonomous Loop)                    │
│  • Experiment Engine (Executor)                      │
│  • Results Tracker (TSV/Git)                         │
│  • Budget Enforcer (Time + Cost)                     │
└──────────────────────┬───────────────────────────────┘
        ┌──────────────┼──────────────┬─────────────┐
        │              │              │             │
        ▼              ▼              ▼             ▼
     Synapse        ADLS Gen2     App Insights   Cost API
     (Queries)     (Storage)      (Monitoring)  (Budget)
```

### Component Interaction

**Autonomous Agent Loop:**
1. Read program constraints (program.md)
2. Check recent results (results.tsv)
3. Ask Claude for proposal
4. Apply changes to analysis.py
5. Git commit
6. Execute with time/cost budget
7. Track metrics
8. Keep if improved, discard if worse
9. Loop (every 5-10 minutes)

### Data Flow

```
User Request
    ↓
FastAPI Endpoint
    ↓
Claude Agent / Experiment Engine
    ↓
Azure Services
    ↓
Application Insights / Cost API
    ↓
Results Tracked (Git + TSV)
    ↓
React Dashboard Updated
    ↓
User Sees Real-Time Metrics
```

---

## 📊 API Endpoints

### Health & Status (3 endpoints)

```bash
GET /                       # Root info
GET /health                 # Health check
GET /api/azure-status       # Azure services status
```

### Programs (4 endpoints)

```bash
GET /api/programs           # List all programs
POST /api/programs          # Create new program
GET /api/programs/{id}      # Get program details
GET /api/programs/{id}/metrics  # Get metrics
```

### Experiments (3 endpoints)

```bash
POST /api/experiments       # Run experiment
GET /api/experiments        # List experiments
GET /api/experiments/{id}   # Get experiment details
```

### Agent (3 endpoints)

```bash
POST /api/agent/propose          # Get Claude proposal
POST /api/agent/start-loop       # Start autonomous loop
POST /api/agent/stop-loop        # Stop autonomous loop
```

### Dashboard (1 endpoint)

```bash
GET /api/dashboard          # Get all dashboard data
```

**Full API Documentation:** http://localhost:8000/docs (Swagger UI)

### Example Requests

**Create Program**
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

**Get Claude Proposal**
```bash
curl -X POST "http://localhost:8000/api/agent/propose?program_id=prog_1"
```

**Run Experiment**
```bash
curl -X POST http://localhost:8000/api/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "program_id": "prog_1",
    "analysis_code": "def get_metric(): return 95.0",
    "description": "Test experiment"
  }'
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18.2
- **Language:** TypeScript 4.9
- **Charts:** Recharts 2.10
- **Styling:** CSS3 + Tailwind (ready)
- **State:** React Hooks
- **HTTP:** Axios

### Backend
- **Framework:** FastAPI 0.104
- **Language:** Python 3.11
- **AI:** Anthropic Claude API (latest)
- **Async:** AsyncIO + Uvicorn
- **Validation:** Pydantic v2

### Cloud & Infrastructure
- **Cloud Provider:** Microsoft Azure
- **Query Engine:** Synapse SQL Pool
- **Data Lake:** ADLS Gen2
- **Monitoring:** Application Insights
- **Cost Tracking:** Cost Management API
- **Secrets:** Azure Key Vault

### DevOps & Deployment
- **Containerization:** Docker 24+
- **Orchestration:** Docker Compose 3.8
- **CI/CD:** GitHub Actions
- **Version Control:** Git
- **Container Registry:** Azure Container Registry (optional)
- **Deployment Targets:** ACI, App Service, AKS

### Development & Testing
- **Testing:** Pytest (Python)
- **Linting:** Flake8, ESLint
- **Formatting:** Black (Python), Prettier (JS)
- **Logging:** Python logging + Console

---

## 📂 Project Structure

```
autopipeline/
├── README.md                          # Main documentation (this file)
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment template
│
├── backend/                           # Python/FastAPI backend
│   ├── backend_main.py               # FastAPI application (main entry)
│   ├── backend_requirements.txt       # Python dependencies
│   └── Dockerfile                     # Backend production image
│
├── frontend/                          # React/TypeScript frontend
│   ├── src/
│   │   ├── App.tsx                   # Main React component
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx     # Dashboard with KPIs & charts
│   │   │   ├── ProgramsPage.tsx      # Programs management
│   │   │   └── ExperimentsPage.tsx   # Experiments tracking
│   │   └── components/
│   │       └── AgentControlPanel.tsx # Agent control interface
│   ├── package.json                   # npm dependencies
│   ├── package-lock.json              # Dependency lock file
│   ├── Dockerfile                     # Frontend production image
│   └── public/                        # Static assets
│
├── docker-compose.yml                 # Local development setup
├── Dockerfile.backend                 # Backend production image
├── Dockerfile.frontend                # Frontend production image
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD pipeline
│
├── CONTRIBUTING.md                    # Contribution guidelines
├── CHANGELOG.md                       # Version history
├── CHANGELOG.md                       # Version history
├── init-repo.sh                       # Repository initialization script
│
└── docs/                              # Documentation (13 files, 50+ pages)
    ├── RUN-NOW.md                    # 5-minute quick start
    ├── SETUP-DEPLOYMENT-GUIDE.md     # Complete setup & deployment
    ├── FULLSTACK-SUMMARY.md          # Platform overview
    ├── IMPLEMENTATION-ROADMAP.md     # 8-week implementation plan
    ├── azure_platform_architecture.md # Technical design with ADRs
    ├── QUICK-GITHUB-SETUP.md         # GitHub setup guide
    ├── GITHUB-SETUP.md               # Full GitHub configuration
    ├── autonomous-data-research-SKILL.md # Operational playbook
    ├── azure_data_platform_proposal.md  # Business proposal
    ├── ARCHITECTURE-DIAGRAMS.md      # 12 Mermaid diagrams
    ├── 00-EXECUTIVE-SUMMARY.md       # Executive summary
    ├── INDEX.md                       # Complete index
    └── START_HERE.txt                # Visual quick reference
```

---

## 🔧 Setup & Deployment

### Local Development

**1. Clone Repository**
```bash
git clone https://github.com/juliopessan/autopipeline.git
cd autopipeline
```

**2. Install Dependencies**

Backend:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/backend_requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

**3. Configure Environment**
```bash
cp .env.example .env
# Edit .env with your credentials
# At minimum: ANTHROPIC_API_KEY=sk-...
```

**4. Run Applications**

Terminal 1 - Backend:
```bash
export ANTHROPIC_API_KEY=sk-your-key
python backend/backend_main.py
# Access: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

Terminal 2 - Frontend:
```bash
cd frontend
npm start
# Access: http://localhost:3000
```

### Docker Deployment

**Local Development with Docker Compose**

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop
docker-compose down
```

### Azure Deployment

See [SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md) for:
- Azure Container Instances (ACI)
- Azure App Service
- Azure Kubernetes Service (AKS)
- Complete infrastructure as code

---

## 📚 Documentation

Comprehensive documentation available in `/docs` folder:

| Document | Purpose | Read Time |
|---|---|---|
| **RUN-NOW.md** | 5-minute quick start | 5 min |
| **SETUP-DEPLOYMENT-GUIDE.md** | Complete setup & deployment guide | 30 min |
| **FULLSTACK-SUMMARY.md** | Platform architecture overview | 15 min |
| **IMPLEMENTATION-ROADMAP.md** | 8-week sprint plan | 20 min |
| **azure_platform_architecture.md** | Technical design with 6 ADRs | 30 min |
| **autonomous-data-research-SKILL.md** | Operational playbook (4 modes) | 20 min |
| **ARCHITECTURE-DIAGRAMS.md** | 12 Mermaid diagrams | 10 min |

**Quick Links:**
- 📖 [Full Documentation Index](docs/INDEX.md)
- 🚀 [Quick Start Guide](docs/RUN-NOW.md)
- 🏗️ [Architecture Design](docs/azure_platform_architecture.md)
- 📋 [Executive Summary](docs/00-EXECUTIVE-SUMMARY.md)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- How to submit issues
- Pull request process
- Development setup

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and commit: `git commit -m 'feat: Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Reporting Issues

Please use GitHub Issues to report bugs. Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python/Node version)

---

## 📊 Performance & Metrics

### Expected Platform Performance

- **Experiment Success Rate:** 85-95%
- **Average Cost per Experiment:** $0.15
- **Time per Experiment:** 5-10 minutes
- **Experiments per Night:** 50-100
- **Typical Improvement:** 5-10% per week
- **Break-even Time:** 2-3 weeks

### Scalability

- **Local Development:** Single machine
- **Docker Compose:** Multi-container orchestration
- **Azure ACI:** Serverless containers (up to 4 vCPU)
- **Azure App Service:** Auto-scaling (1-20+ instances)
- **Azure AKS:** Enterprise Kubernetes (unlimited)

---

## 🔐 Security

### Built-in Security Features

- Environment variable-based secrets (no hardcoding)
- Azure service principal authentication
- CORS configuration
- API endpoint validation
- Health checks and monitoring
- Error handling and logging
- Azure Key Vault integration
- Managed identity support

### Best Practices

- Regenerate secrets regularly
- Use Personal Access Tokens for GitHub
- Enable branch protection on main
- Review code before merging
- Monitor costs regularly
- Keep dependencies updated

---

## 📈 Roadmap

### Completed (v1.0)
- ✅ Autonomous agent loop
- ✅ Real-time dashboard
- ✅ Budget enforcement
- ✅ Azure integration
- ✅ Docker containerization
- ✅ GitHub Actions CI/CD
- ✅ Comprehensive documentation

### Planned (v1.1 - Q2 2025)
- [ ] PostgreSQL database integration
- [ ] Advanced analytics dashboard
- [ ] Webhook integrations
- [ ] Unit & integration tests

### Planned (v2.0 - Q3 2025)
- [ ] Multi-agent swarms
- [ ] Advanced ML features
- [ ] Customer platform
- [ ] API marketplace

### Planned (v3.0+)
- [ ] Enterprise SSO
- [ ] Advanced compliance
- [ ] Custom models
- [ ] Global scale

See [IMPLEMENTATION-ROADMAP.md](docs/IMPLEMENTATION-ROADMAP.md) for detailed 8-week plan.

---

## 📞 Support & Help

### Getting Help

- **Documentation:** See [docs/](docs/) folder (50+ pages)
- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Issues:** GitHub Issues for bug reports
- **Discussions:** GitHub Discussions for questions
- **Email:** julio@fcamara.com.br

### Troubleshooting

**Backend won't start?**
```bash
pip install -r backend/backend_requirements.txt
python backend/backend_main.py
```

**Frontend won't build?**
```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

**Azure not connecting?**
Don't worry! Platform runs in mock mode. Set Azure env vars to use real services.

See [SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md) troubleshooting section for more.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Summary:** You are free to use, modify, and distribute this software, provided you include the original copyright notice and license.

---

## 👥 Authors & Contributors

### Lead Author
- **Julio Pessan** - AI Solutions Architect @ FCamara
  - LinkedIn: [juliopessan](https://linkedin.com/in/juliopessan)
  - GitHub: [@juliopessan](https://github.com/juliopessan)
  - Email: julio@fcamara.com.br

### Acknowledgments

- Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch)
- Powered by [Anthropic Claude](https://claude.ai)
- Built with [FastAPI](https://fastapi.tiangolo.com) & [React](https://react.dev)
- Deployed on [Microsoft Azure](https://azure.microsoft.com)
- Open sourced by [FCamara](https://fcamara.com.br)

---

## 📊 Repository Statistics

- **Language:** Python + TypeScript
- **Files:** 39
- **Code Lines:** 2,000+
- **Documentation:** 50+ pages
- **API Endpoints:** 15
- **Frontend Pages:** 4
- **Docker Images:** 2
- **CI/CD Workflows:** 1
- **Test Coverage:** Ready to add
- **License:** MIT

---

## 🚀 Getting Started

1. **Read:** [RUN-NOW.md](docs/RUN-NOW.md) (5 minutes)
2. **Clone:** `git clone https://github.com/juliopessan/autopipeline.git`
3. **Install:** Backend + Frontend dependencies
4. **Configure:** Create `.env` from `.env.example`
5. **Run:** `python backend_main.py` & `npm start`
6. **Explore:** Visit http://localhost:3000

---

## 🎯 Next Steps

### For Users
1. Deploy locally
2. Create optimization programs
3. Run experiments
4. Monitor dashboard
5. Deploy to Azure

### For Developers
1. Fork repository
2. Set up development environment
3. Check [CONTRIBUTING.md](CONTRIBUTING.md)
4. Create feature branch
5. Submit pull request

### For Enterprises
1. Review [SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md)
2. Deploy on Azure AKS
3. Configure SSO & compliance
4. Set up monitoring & alerts
5. Train team on operations

---

<div align="center">

**Made with ❤️ by FCamara**

[⭐ Star this repository](https://github.com/juliopessan/autopipeline) if you find it useful!

[Report a Bug](https://github.com/juliopessan/autopipeline/issues) · [Request a Feature](https://github.com/juliopessan/autopipeline/issues) · [View Documentation](docs/)

---

**Azure Autonomous Data Platform** · v1.0 · March 2025

</div>

