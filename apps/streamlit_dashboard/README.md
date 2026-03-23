# 🤖 Azure Autonomous Data Platform - Streamlit Dashboard

Modern Python dashboard built with Streamlit for the Azure Autonomous Data Platform.

## Features

- 📊 **Real-time Dashboard** - KPI cards, charts, metrics
- 📈 **Experiments Tracking** - View and create experiments
- 💼 **Programs Management** - Manage optimization programs
- ⚙️ **Settings** - Configure application
- 🐍 **100% Python** - No JavaScript needed!

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py

# Opens at http://localhost:8501
```

### With Docker

```bash
docker build -t autopipeline-dashboard .
docker run -p 8501:8501 autopipeline-dashboard
```

## Structure

```
apps/streamlit_dashboard/
├── app.py              # Main application
├── pages/              # Multi-page apps
│   ├── dashboard.py    # Dashboard page
│   ├── experiments.py  # Experiments page
│   ├── programs.py     # Programs page
│   └── settings.py     # Settings page
├── lib/                # Utility libraries
│   ├── api_client.py   # FastAPI client
│   ├── charts.py       # Plotly charts
│   └── utils.py        # Helper functions
├── .streamlit/
│   └── config.toml     # Streamlit configuration
└── requirements.txt
```

## Configuration

### Environment Variables

```bash
BACKEND_URL=http://localhost:8000    # FastAPI backend
STREAMLIT_SERVER_PORT=8501           # Port
STREAMLIT_SERVER_HEADLESS=true       # Headless mode
```

### Streamlit Config

Edit `.streamlit/config.toml`:
- Theme colors
- Server settings
- Client behavior

## API Integration

Dashboard communicates with FastAPI backend:

```python
from lib.api_client import get_api_client

api = get_api_client()
data = api.get_dashboard()
programs = api.get_programs()
```

## Deployment

### Streamlit Cloud

```bash
# Push to GitHub
git push origin main

# Go to https://streamlit.io/cloud
# Connect GitHub repo
# Deploy!
```

### Docker Compose

```bash
docker-compose up streamlit_dashboard
```

### Azure App Service

```bash
az webapp create --resource-group mygroup --plan myplan --name myapp
az webapp deployment source config-zip --resource-group mygroup --name myapp --src deploy.zip
```

## Development

### Add New Page

1. Create `pages/new_page.py`:
```python
import streamlit as st

def show():
    st.subheader("My Page")
    st.write("Content here")
```

2. Add to navigation in `app.py`:
```python
page = st.radio("Select page:", [
    "📊 Dashboard",
    "🆕 My Page",  # Add here
    ...
])
```

### Add New Chart

1. Add to `lib/charts.py`:
```python
import plotly.graph_objects as go

def my_chart(data):
    return go.Figure(...)
```

2. Use in pages:
```python
from lib.charts import my_chart

fig = my_chart(data)
st.plotly_chart(fig, use_container_width=True)
```

## Performance

- **Load Time**: <1 second
- **HMR**: Auto-refresh on file save
- **Memory**: ~200MB baseline
- **Responsive**: Works on mobile/tablet/desktop

## Troubleshooting

### Backend Connection Error

```
❌ Backend Offline
```

Make sure FastAPI is running:
```bash
python apps/backend/main.py
```

### Streamlit Cache Issues

```bash
rm -rf ~/.streamlit/
streamlit run app.py
```

### Port Already in Use

```bash
lsof -ti:8501 | xargs kill -9
streamlit run app.py
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Charts](https://plotly.com/python/)
- [FastAPI Integration](https://fastapi.tiangolo.com/)

---

**Status**: ✅ Production Ready  
**Python**: 3.11+  
**License**: MIT
