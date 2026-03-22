import React, { useState, useEffect } from 'react';
import './App.css';

interface Program {
  id: string;
  name: string;
  constraints: string;
  optimization_goal: string;
  metric_name: string;
  baseline_value: number;
  target_value: number;
  max_iterations: number;
}

interface DashboardData {
  total_experiments: number;
  successful_experiments: number;
  failed_experiments: number;
  success_rate: number;
  total_cost: number;
  budget_remaining: number;
  programs: Program[];
}

function App() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dashboard');
        if (!response.ok) throw new Error('Failed to fetch dashboard data');
        const data = await response.json();
        setDashboardData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error Loading Dashboard</h2>
          <p>{error}</p>
          <p style={{ marginTop: '20px', fontSize: '14px' }}>
            Make sure the backend is running at http://localhost:8000
          </p>
          <p style={{ marginTop: '10px', fontSize: '14px' }}>
            Run: <code>python backend/backend_main.py</code>
          </p>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="app">
        <div className="loading">No dashboard data available</div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 Azure Autonomous Data Platform</h1>
        <p>AI-powered pipeline optimization dashboard</p>
      </header>

      <main className="dashboard">
        <section className="kpi-cards">
          <div className="card">
            <div className="label">Total Experiments</div>
            <div className="value">{dashboardData.total_experiments}</div>
          </div>
          <div className="card">
            <div className="label">Success Rate</div>
            <div className="value">{(dashboardData.success_rate * 100).toFixed(1)}%</div>
          </div>
          <div className="card">
            <div className="label">Total Cost</div>
            <div className="value">${dashboardData.total_cost.toFixed(2)}</div>
          </div>
          <div className="card">
            <div className="label">Budget Remaining</div>
            <div className="value">${dashboardData.budget_remaining.toFixed(2)}</div>
          </div>
          <div className="card">
            <div className="label">Successful</div>
            <div className="value" style={{ color: '#4CAF50' }}>
              {dashboardData.successful_experiments}
            </div>
          </div>
          <div className="card">
            <div className="label">Failed</div>
            <div className="value" style={{ color: '#f44336' }}>
              {dashboardData.failed_experiments}
            </div>
          </div>
        </section>

        <section className="programs">
          <h2>Active Programs</h2>
          {dashboardData.programs.length === 0 ? (
            <p style={{ color: '#666' }}>No programs yet. Create one to get started!</p>
          ) : (
            <div className="program-list">
              {dashboardData.programs.map((program) => (
                <div key={program.id} className="program-card">
                  <h3>{program.name}</h3>
                  <p><strong>Goal:</strong> {program.optimization_goal}</p>
                  <p><strong>Metric:</strong> {program.metric_name}</p>
                  <p><strong>Baseline:</strong> {program.baseline_value} → Target: {program.target_value}</p>
                  <p><strong>Max Iterations:</strong> {program.max_iterations}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="info">
          <h2>ℹ️ Quick Links</h2>
          <ul>
            <li><a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">📚 API Documentation (Swagger)</a></li>
            <li><a href="https://github.com/juliopessan/autopipeline" target="_blank" rel="noopener noreferrer">🐙 GitHub Repository</a></li>
            <li><a href="https://github.com/juliopessan/autopipeline/tree/main/docs" target="_blank" rel="noopener noreferrer">📖 Documentation</a></li>
          </ul>
        </section>
      </main>
    </div>
  );
}

export default App;
