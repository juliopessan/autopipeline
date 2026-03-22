import React, { useState, useEffect } from 'react';
import './App.css';
import DashboardPage from './pages/DashboardPage';
import ProgramsPage from './pages/ProgramsPage';
import ExperimentsPage from './pages/ExperimentsPage';
import AgentControlPanel from './components/AgentControlPanel';

type PageType = 'dashboard' | 'programs' | 'experiments' | 'agent';

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('dashboard');
  const [loading, setLoading] = useState(false);
  const [azureConnected, setAzureConnected] = useState(false);

  useEffect(() => {
    // Check Azure status on load
    fetch('http://localhost:8000/api/azure-status')
      .then(res => res.json())
      .then(data => {
        setAzureConnected(data.synapse === 'connected');
      })
      .catch(() => setAzureConnected(false));
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'programs':
        return <ProgramsPage />;
      case 'experiments':
        return <ExperimentsPage />;
      case 'agent':
        return <AgentControlPanel />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🤖</span>
            <h1>Azure Autonomous Data Platform</h1>
          </div>
          <div className="header-status">
            <div className={`status-badge ${azureConnected ? 'connected' : 'disconnected'}`}>
              <span className="status-dot"></span>
              {azureConnected ? 'Azure Connected' : 'Mock Mode'}
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="app-nav">
        <div className="nav-content">
          <button
            className={`nav-button ${currentPage === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentPage('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`nav-button ${currentPage === 'programs' ? 'active' : ''}`}
            onClick={() => setCurrentPage('programs')}
          >
            📋 Programs
          </button>
          <button
            className={`nav-button ${currentPage === 'experiments' ? 'active' : ''}`}
            onClick={() => setCurrentPage('experiments')}
          >
            ⚗️ Experiments
          </button>
          <button
            className={`nav-button ${currentPage === 'agent' ? 'active' : ''}`}
            onClick={() => setCurrentPage('agent')}
          >
            🤖 Agent Control
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="app-main">
        {renderPage()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>&copy; 2025 Azure Autonomous Data Platform by FCamara</p>
          <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
            API Docs
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;
