import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './DashboardPage.css';

interface DashboardData {
  programs: Program[];
  recent_experiments: Experiment[];
  system_health: {
    agent_running: boolean;
    total_experiments: number;
    success_rate: number;
    status: string;
  };
  cost_summary: {
    total_cost_usd: number;
    avg_per_experiment: number;
    budget_remaining: number;
  };
}

interface Program {
  id: string;
  name: string;
  status: string;
  metric_name: string;
  baseline_value: number;
  created_at: string;
}

interface Experiment {
  id: string;
  program_id: string;
  metric: number;
  cost_usd: number;
  status: string;
  created_at: string;
}

const DashboardPage: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshInterval, setRefreshInterval] = useState(5000); // 5 seconds

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dashboard');
        if (!response.ok) throw new Error('Failed to fetch dashboard');
        const data = await response.json();
        setDashboard(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
    const interval = setInterval(fetchDashboard, refreshInterval);

    return () => clearInterval(interval);
  }, [refreshInterval]);

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error || !dashboard) {
    return <div className="dashboard-error">Error: {error || 'No data'}</div>;
  }

  // Prepare chart data
  const metricTrendData = dashboard.recent_experiments
    .reverse()
    .map((exp, idx) => ({
      name: `Exp ${idx + 1}`,
      metric: parseFloat(exp.metric.toFixed(2)),
      cost: parseFloat(exp.cost_usd.toFixed(2)),
    }));

  const costData = [
    { name: 'Total Cost', value: dashboard.cost_summary.total_cost_usd },
    { name: 'Budget Remaining', value: dashboard.cost_summary.budget_remaining },
  ];

  return (
    <div className="dashboard">
      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-label">Total Experiments</div>
          <div className="kpi-value">{dashboard.system_health.total_experiments}</div>
          <div className="kpi-subtitle">Completed</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Success Rate</div>
          <div className="kpi-value">{dashboard.system_health.success_rate.toFixed(1)}%</div>
          <div className="kpi-subtitle">Successful runs</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Total Cost</div>
          <div className="kpi-value">${dashboard.cost_summary.total_cost_usd.toFixed(2)}</div>
          <div className="kpi-subtitle">USD spent</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Avg Cost/Exp</div>
          <div className="kpi-value">${dashboard.cost_summary.avg_per_experiment.toFixed(2)}</div>
          <div className="kpi-subtitle">Per experiment</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Budget Remaining</div>
          <div className="kpi-value">${dashboard.cost_summary.budget_remaining.toFixed(2)}</div>
          <div className="kpi-subtitle">Available</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Agent Status</div>
          <div className={`kpi-value ${dashboard.system_health.agent_running ? 'running' : 'stopped'}`}>
            {dashboard.system_health.agent_running ? '🟢 Running' : '🔴 Stopped'}
          </div>
          <div className="kpi-subtitle">Autonomous loop</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Metric Trend Chart */}
        <div className="chart-container">
          <h3>Metric Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metricTrendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="metric"
                stroke="#4CAF50"
                dot={{ fill: '#4CAF50', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Cost Chart */}
        <div className="chart-container">
          <h3>Cost Summary</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={costData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#2196F3" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Experiments Table */}
      <div className="section">
        <h3>Recent Experiments</h3>
        <div className="table-container">
          <table className="experiments-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Program</th>
                <th>Metric</th>
                <th>Cost</th>
                <th>Status</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {dashboard.recent_experiments.map((exp) => (
                <tr key={exp.id} className={`status-${exp.status}`}>
                  <td className="mono">{exp.id.substring(0, 8)}</td>
                  <td>{exp.program_id}</td>
                  <td className="metric">{parseFloat(exp.metric.toFixed(4))}</td>
                  <td className="cost">${exp.cost_usd.toFixed(2)}</td>
                  <td>
                    <span className={`status-badge status-${exp.status}`}>
                      {exp.status}
                    </span>
                  </td>
                  <td className="small">
                    {new Date(exp.created_at).toLocaleTimeString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Programs Overview */}
      <div className="section">
        <h3>Active Programs ({dashboard.programs.length})</h3>
        <div className="programs-grid">
          {dashboard.programs.map((program) => (
            <div key={program.id} className="program-card">
              <h4>{program.name}</h4>
              <div className="program-info">
                <div className="info-item">
                  <span className="label">Metric:</span>
                  <span className="value">{program.metric_name}</span>
                </div>
                <div className="info-item">
                  <span className="label">Baseline:</span>
                  <span className="value">{program.baseline_value}</span>
                </div>
                <div className="info-item">
                  <span className="label">Status:</span>
                  <span className={`status-${program.status}`}>{program.status}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Refresh Control */}
      <div className="dashboard-controls">
        <label>
          Auto-refresh interval:
          <select value={refreshInterval} onChange={(e) => setRefreshInterval(Number(e.target.value))}>
            <option value={2000}>2 seconds</option>
            <option value={5000}>5 seconds</option>
            <option value={10000}>10 seconds</option>
            <option value={30000}>30 seconds</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default DashboardPage;
