import React, { useState, useEffect } from 'react';
import './AgentControlPanel.css';

interface Program {
  id: string;
  name: string;
  optimization_goal: string;
}

const AgentControlPanel: React.FC = () => {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [selectedProgram, setSelectedProgram] = useState<string>('');
  const [agentRunning, setAgentRunning] = useState(false);
  const [proposal, setProposal] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    // Load programs
    fetch('http://localhost:8000/api/programs')
      .then(res => res.json())
      .then(data => {
        setPrograms(data);
        if (data.length > 0) setSelectedProgram(data[0].id);
      })
      .catch(err => setMessage(`Error loading programs: ${err}`));
  }, []);

  const handleGetProposal = async () => {
    if (!selectedProgram) {
      setMessage('Please select a program');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/agent/propose?program_id=${selectedProgram}`,
        { method: 'POST' }
      );

      if (!response.ok) throw new Error('Failed to get proposal');
      const data = await response.json();
      setProposal(data);
      setMessage('Got proposal from Claude!');
    } catch (err) {
      setMessage(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleStartAgent = async () => {
    if (!selectedProgram) {
      setMessage('Please select a program');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/agent/start-loop`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ program_id: selectedProgram }),
        }
      );

      if (!response.ok) throw new Error('Failed to start agent');
      setAgentRunning(true);
      setMessage('Agent loop started!');
    } catch (err) {
      setMessage(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleStopAgent = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        'http://localhost:8000/api/agent/stop-loop',
        { method: 'POST' }
      );

      if (!response.ok) throw new Error('Failed to stop agent');
      setAgentRunning(false);
      setMessage('Agent loop stopped');
    } catch (err) {
      setMessage(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="agent-control">
      <h2>🤖 Autonomous Agent Control</h2>

      {/* Program Selection */}
      <div className="control-section">
        <h3>Select Program</h3>
        <div className="form-group">
          <label>Program:</label>
          <select
            value={selectedProgram}
            onChange={(e) => setSelectedProgram(e.target.value)}
            disabled={loading}
          >
            <option value="">-- Select Program --</option>
            {programs.map((prog) => (
              <option key={prog.id} value={prog.id}>
                {prog.name} ({prog.id})
              </option>
            ))}
          </select>
        </div>

        {selectedProgram && (
          <div className="program-info">
            <p>
              <strong>Goal:</strong>{' '}
              {programs.find(p => p.id === selectedProgram)?.optimization_goal}
            </p>
          </div>
        )}
      </div>

      {/* Agent Controls */}
      <div className="control-section">
        <h3>Agent Status</h3>
        <div className="status-display">
          <div className={`status-indicator ${agentRunning ? 'running' : 'stopped'}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {agentRunning ? 'Agent Running' : 'Agent Stopped'}
            </span>
          </div>
        </div>

        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={handleStartAgent}
            disabled={loading || agentRunning}
          >
            {loading ? 'Starting...' : '▶️ Start Agent Loop'}
          </button>
          <button
            className="btn btn-danger"
            onClick={handleStopAgent}
            disabled={!agentRunning || loading}
          >
            {loading ? 'Stopping...' : '⏹️ Stop Agent Loop'}
          </button>
        </div>
      </div>

      {/* Get Proposal */}
      <div className="control-section">
        <h3>Manual Proposal Request</h3>
        <p className="description">
          Ask Claude for an optimization proposal without running full experiment loop
        </p>

        <button
          className="btn btn-secondary"
          onClick={handleGetProposal}
          disabled={loading || !selectedProgram}
        >
          {loading ? 'Getting proposal...' : '💡 Get Claude Proposal'}
        </button>

        {proposal && (
          <div className="proposal-display">
            <h4>Claude's Proposal</h4>
            <div className="proposal-item">
              <label>Idea:</label>
              <p>{proposal.idea}</p>
            </div>
            <div className="proposal-item">
              <label>Rationale:</label>
              <p>{proposal.rationale}</p>
            </div>
            <div className="proposal-item">
              <label>Code:</label>
              <pre>
                <code>{proposal.code}</code>
              </pre>
            </div>
          </div>
        )}
      </div>

      {/* Agent Info */}
      <div className="control-section info-section">
        <h3>📋 Agent Information</h3>
        <div className="info-box">
          <p>
            <strong>Role:</strong> Autonomous data pipeline researcher
          </p>
          <p>
            <strong>Capability:</strong> Proposes improvements, runs experiments,
            tracks metrics
          </p>
          <p>
            <strong>Status:</strong> {agentRunning ? '✅ Active' : '⏸️ Inactive'}
          </p>
          <p>
            <strong>Loop Interval:</strong> Every 5-10 minutes per experiment
          </p>
          <p>
            <strong>Time Budget:</strong> 10 minutes per experiment
          </p>
          <p>
            <strong>Cost Limit:</strong> $5 per experiment
          </p>
        </div>
      </div>

      {/* Messages */}
      {message && (
        <div className={`message-box ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default AgentControlPanel;
