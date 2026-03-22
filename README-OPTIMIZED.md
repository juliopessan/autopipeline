# 🤖 Azure Autonomous Data Platform

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen?style=flat-square)](https://github.com/juliopessan/autopipeline)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-18%2B-green?style=flat-square)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-24%2B-blue?style=flat-square)](https://www.docker.com/)

**Production-ready autonomous data pipeline optimization platform powered by Claude AI and Microsoft Azure**

---

## 🎯 What is This?

A fullstack platform that uses Claude AI to **autonomously optimize data pipelines** while you keep complete control. 

- **Autonomous**: Claude proposes improvements automatically
- **Safe**: Budget enforcement & success-based logic (keep if better, discard if worse)
- **Observable**: Real-time dashboard shows everything
- **Enterprise-Ready**: Docker, GitHub Actions, Azure integration

---

## ✨ Key Features

🤖 **Autonomous Optimization**
- Claude AI proposes improvements without waiting for approval
- Time & cost budget enforcement (prevents runaway experiments)
- Continuous improvement loop running 24/7

📊 **Real-Time Dashboard**
- 6 KPI cards (experiments, success rate, costs, budget)
- Interactive charts and metrics
- Program and experiment tracking
- Live updates every 5 seconds

💼 **Full Management**
- Create and manage optimization programs
- Track all experiments and results
- View Claude proposals before execution
- Control autonomous loop (start/stop)

🔗 **Azure Integration**
- Synapse SQL, ADLS Gen2, Application Insights, Cost Management API
- Mock mode for local testing (no Azure credentials needed)

---

## 🚀 Quick Start

### Prerequisites
```bash
python3 --version    # Need 3.11+
node --version       # Need 18+
git clone https://github.com/juliopessan/autopipeline.git
cd autopipeline
```

### Option 1: Local (Recommended)
```bash
# Terminal 1 - Backend
python3 -m venv venv
source venv/bin/activate
pip install -r backend/backend_requirements.txt
export ANTHROPIC_API_KEY=sk-your-key-here
python backend/backend_main.py
# Opens: http://localhost:8000
```

```bash
# Terminal 2 - Frontend
cd frontend
npm install
npm start
# Opens: http://localhost:3000
```

### Option 2: Docker
```bash
cp .env.example .env
# Edit .env with ANTHROPIC_API_KEY
docker-compose up
```

➡️ **Full Setup Guide**: See [docs/RUN-NOW.md](docs/RUN-NOW.md)

---

## 📊 Architecture

```
React Dashboard        FastAPI Backend       Azure Services
(http://3000)  ←→     (http://8000)    ←→   (Synapse, ADLS, Insights)
                          ↓
                    Claude AI Agent
                    (Autonomous Loop)
```

**15 REST API endpoints** • **Swagger docs at `/docs`** • Full async/await

➡️ **Detailed Architecture**: See [docs/azure_platform_architecture.md](docs/azure_platform_architecture.md)

---

## 📁 Project Structure

```
autopipeline/
├── backend/              # FastAPI application (500+ lines)
│   ├── backend_main.py
│   └── backend_requirements.txt
├── frontend/             # React application (300+ lines)
│   ├── src/App.tsx
│   └── package.json
├── docker-compose.yml    # Local development
├── docs/                 # 24 files, 50+ pages
│   ├── RUN-NOW.md (5-minute quick start)
│   ├── SETUP-DEPLOYMENT-GUIDE.md (complete)
│   ├── IMPLEMENTATION-ROADMAP.md (8-week plan)
│   └── ...13 more guides
├── README.md             # This file
└── LICENSE              # MIT
```

**Complete file inventory**: See [docs/MANIFEST.md](docs/MANIFEST.md)

---

## 🛠 Technology Stack

| Layer | Tech |
|-------|------|
| **Frontend** | React 18 + TypeScript 4.9 + Recharts |
| **Backend** | FastAPI 0.104 + Python 3.11 + Anthropic Claude |
| **Cloud** | Azure (Synapse, ADLS, Insights, Cost API) |
| **DevOps** | Docker 24+, Docker Compose, GitHub Actions |

---

## 📚 Documentation

| Guide | Purpose | Time |
|-------|---------|------|
| [RUN-NOW.md](docs/RUN-NOW.md) | Get running locally | 5 min |
| [SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md) | Deploy to Azure | 30 min |
| [azure_platform_architecture.md](docs/azure_platform_architecture.md) | Technical design + 6 ADRs | 45 min |
| [IMPLEMENTATION-ROADMAP.md](docs/IMPLEMENTATION-ROADMAP.md) | 8-week sprint plan | 20 min |
| [MACOS-SETUP-GUIDE.md](docs/MACOS-SETUP-GUIDE.md) | macOS specific help | 15 min |

**Full Documentation Index**: See [docs/00-PROJECT-INDEX.md](docs/00-PROJECT-INDEX.md)

---

## 💡 How It Works

1. **Create Program** → Define optimization goal + constraints
2. **Claude Proposes** → AI suggests improvements (every 5-10 min)
3. **Experiment Runs** → System executes with time/cost budget
4. **Metrics Tracked** → Results saved in Git + TSV
5. **Keep or Discard** → If metrics improved, keep; otherwise revert
6. **Loop Continues** → Repeat until stopped

All decisions tracked in Git. All improvements auditable.

---

## 🎯 Status & Roadmap

**v1.0 - Current (Production Ready)**
- ✅ Autonomous agent loop
- ✅ Real-time dashboard
- ✅ Azure integration
- ✅ Docker setup
- ✅ Complete documentation

**v1.1 - Planned (Q2 2025)**
- PostgreSQL integration
- Advanced analytics
- Webhook support
- Unit/integration tests

➡️ **Full Roadmap**: See [docs/IMPLEMENTATION-ROADMAP.md](docs/IMPLEMENTATION-ROADMAP.md)

---

## 📊 Project Stats

- **Code**: 2,000+ lines (backend + frontend)
- **Documentation**: 50+ pages across 24 files
- **Tests**: Ready for your test suite
- **License**: MIT (open source)
- **Status**: Production ready

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- How to submit issues
- Pull request process

---

## 📞 Support & Troubleshooting

**Can't get it running?**
- macOS issues? → [docs/MACOS-SETUP-GUIDE.md](docs/MACOS-SETUP-GUIDE.md)
- Deployment questions? → [docs/SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md)
- General help? → [docs/00-PROJECT-INDEX.md](docs/00-PROJECT-INDEX.md)

**GitHub Issues**: Report bugs or request features

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file. Free to use, modify, and distribute.

---

## 👥 Authors

**Julio Pessan** - AI Solutions Architect @ FCamara
- [GitHub](https://github.com/juliopessan)
- [LinkedIn](https://linkedin.com/in/juliopessan)

Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch)

---

## 🚀 Next Steps

1. **Run it**: `cd autopipeline && npm install && npm start`
2. **Read docs**: Start with [docs/RUN-NOW.md](docs/RUN-NOW.md)
3. **Deploy it**: Follow [docs/SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md)
4. **Extend it**: Build on the foundation with your improvements

---

<div align="center">

**Built with ❤️ for the open source community**

[⭐ Star this repo](https://github.com/juliopessan/autopipeline) if you find it useful!

</div>
