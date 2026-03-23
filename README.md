# 🤖 Azure Autonomous Data Platform

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen?style=flat-square)](https://github.com/juliopessan/autopipeline)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28-red?style=flat-square)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-24%2B-blue?style=flat-square)](https://www.docker.com/)

**Production-ready autonomous data pipeline optimization platform powered by Claude AI, FastAPI, and Streamlit**

---

## 🎯 What is This?

A fullstack platform that uses Claude AI to **autonomously optimize data pipelines** while you keep complete control.

- **Autonomous**: Claude proposes improvements automatically
- **Safe**: Budget enforcement & success-based logic (keep if better, discard if worse)
- **Observable**: Real-time Streamlit dashboard shows everything
- **100% Python**: Dashboard in pure Python with Streamlit (perfect for data scientists!)
- **Enterprise-Ready**: Docker, GitHub Actions, Azure integration

---

## ✨ Key Features

🤖 **Autonomous Optimization**
- Claude AI proposes improvements without waiting for approval
- Time & cost budget enforcement (prevents runaway experiments)
- Continuous improvement loop running 24/7

📊 **Real-Time Streamlit Dashboard** ⭐ NEW!
- 4 KPI cards (experiments, success rate, costs, budget)
- Interactive charts with Plotly
- Program and experiment tracking
- Settings and configuration
- **Zero JavaScript needed!** 🐍

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
docker --version     # Optional but recommended
```

### Option 1: Local (Recommended for Data Scientists)

```bash
# Terminal 1 - Backend (FastAPI)
cd apps/backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-your-key-here
python main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

```bash
# Terminal 2 - Dashboard (Streamlit)
cd apps/streamlit_dashboard
pip install -r requirements.txt
streamlit run app.py
# Dashboard: http://localhost:8501
```

### Option 2: Docker Compose

```bash
cp .env.example .env
# Edit .env with ANTHROPIC_API_KEY

docker-compose up

# Backend:   http://localhost:8000
# Dashboard: http://localhost:8501
```

➡️ **Full Setup Guide**: See [docs/RUN-NOW.md](docs/RUN-NOW.md)

---

## 📊 Architecture

```
Streamlit Dashboard     FastAPI Backend        Azure Services
(http://8501)   ←→     (http://8000)    ←→   (Synapse, ADLS, Insights)
    🐍 Python              🐍 Python
    
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
├── apps/
│   ├── backend/                   (FastAPI - Python)
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── streamlit_dashboard/       (Streamlit - Python) ⭐ NEW!
│       ├── app.py                 (Main dashboard)
│       ├── pages/                 (Multi-page)
│       │   ├── dashboard.py       (KPIs & charts)
│       │   ├── experiments.py     (Tracking)
│       │   ├── programs.py        (Management)
│       │   └── settings.py        (Config)
│       ├── lib/                   (Utilities)
│       │   ├── api_client.py      (FastAPI client)
│       │   ├── charts.py          (Plotly charts)
│       │   └── utils.py           (Helpers)
│       ├── requirements.txt
│       └── Dockerfile
├── docker-compose.yml             (Updated)
├── scripts/
│   ├── build.sh
│   └── dev.sh
├── docs/                          (50+ pages)
│   ├── STREAMLIT-MIGRATION.md    (⭐ NEW)
│   ├── RUN-NOW.md
│   └── ...
└── README.md
```

**Complete file inventory**: See [docs/MANIFEST.md](docs/MANIFEST.md)

---

## 🛠 Technology Stack

| Layer | Tech | Why? |
|-------|------|------|
| **Frontend** | Streamlit | 🐍 Python! No JavaScript |
| **Backend** | FastAPI + Python | Modern, async, type-safe |
| **AI** | Claude (Anthropic) | State-of-the-art autonomous agent |
| **Cloud** | Azure (Synapse, ADLS, Insights) | Enterprise-grade infrastructure |
| **DevOps** | Docker, Docker Compose | Reproducible deployments |

---

## 📚 Documentation

| Guide | Purpose | Time |
|-------|---------|------|
| [RUN-NOW.md](docs/RUN-NOW.md) | Get running locally | 5 min |
| [STREAMLIT-MIGRATION.md](docs/STREAMLIT-MIGRATION.md) | ⭐ NEW - Streamlit guide | 10 min |
| [SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md) | Deploy to Azure | 30 min |
| [azure_platform_architecture.md](docs/azure_platform_architecture.md) | Technical design + ADRs | 45 min |
| [IMPLEMENTATION-ROADMAP.md](docs/IMPLEMENTATION-ROADMAP.md) | 8-week sprint plan | 20 min |

**Full Documentation Index**: See [docs/00-PROJECT-INDEX.md](docs/00-PROJECT-INDEX.md)

---

## 💡 How It Works

1. **Create Program** → Define optimization goal + constraints (Streamlit UI)
2. **Claude Proposes** → AI suggests improvements (every 5-10 min)
3. **Experiment Runs** → System executes with time/cost budget
4. **Metrics Tracked** → Results saved in Git + TSV (observable!)
5. **Keep or Discard** → If metrics improved, keep; otherwise revert
6. **Loop Continues** → Repeat until stopped

All decisions tracked in Git. All improvements auditable.

---

## 🎯 Status & Roadmap

**v1.0 - Current (Production Ready) ✅**
- ✅ Autonomous agent loop
- ✅ Real-time Streamlit dashboard
- ✅ Azure integration
- ✅ Docker setup
- ✅ Complete documentation
- ✅ 100% Python stack

**v1.1 - Planned (Q2 2025)**
- Streamlit authentication
- PostgreSQL integration
- Advanced ML analytics
- Webhook support

➡️ **Full Roadmap**: See [docs/IMPLEMENTATION-ROADMAP.md](docs/IMPLEMENTATION-ROADMAP.md)

---

## 📊 Project Stats

- **Code**: 3,000+ lines (backend + dashboard)
- **Documentation**: 50+ pages across 24 files
- **Stack**: 100% Python 🐍
- **Dashboard**: Streamlit (super fast!)
- **Tests**: Ready for your test suite
- **License**: MIT (open source)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- How to submit issues
- Pull request process

---

## 📞 Support & Troubleshooting

**Getting started?**
- Python beginners? → [docs/RUN-NOW.md](docs/RUN-NOW.md)
- Streamlit questions? → [docs/STREAMLIT-MIGRATION.md](docs/STREAMLIT-MIGRATION.md)
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

1. **Run it**: `docker-compose up`
2. **Access Dashboard**: http://localhost:8501
3. **Read Streamlit Guide**: [docs/STREAMLIT-MIGRATION.md](docs/STREAMLIT-MIGRATION.md)
4. **Deploy to Cloud**: Follow [docs/SETUP-DEPLOYMENT-GUIDE.md](docs/SETUP-DEPLOYMENT-GUIDE.md)

---

<div align="center">

**Built with ❤️ for data scientists, by data scientists**

[⭐ Star this repo](https://github.com/juliopessan/autopipeline) if you find it useful!

🐍 **100% Python Stack** | 📊 **Streamlit Dashboard** | 🤖 **Claude AI** | ☁️ **Azure Native**

</div>
