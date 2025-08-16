import React, { useState, useEffect } from 'react';
import axios from '../lib/axios';

export default function AssistantWidget() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load history from localStorage when component mounts
  useEffect(() => {
    const saved = localStorage.getItem('assistantHistory');
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  // Save history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('assistantHistory', JSON.stringify(history));
  }, [history]);

  async function ask() {
    if (!q.trim()) return;
    setLoading(true);
    const currentQuestion = q;
    try {
      const res = await axios.post('/assistant/ask/', { query_text: currentQuestion });
      // Ensure both question and response are saved
      setHistory(prev => [
        { query_text: currentQuestion, response_text: res.data.response_text || 'No response' },
        ...prev
      ]);
      setQ('');
    } catch (err) {
      console.error(err);
      setHistory(prev => [
        { query_text: currentQuestion, response_text: 'Error contacting assistant.' },
        ...prev
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="position-fixed" style={{ right: 20, bottom: 20, zIndex: 1050 }}>
      <div className="card" style={{ width: 320 }}>
        <div className="card-body p-2">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <strong>Assistant</strong>
            <button 
              className="btn btn-sm btn-light" 
              onClick={() => setOpen(!open)}
            >
              {open ? '—' : '+'}
            </button>
          </div>

          {open && (
            <>
              <div style={{ maxHeight: 200, overflowY: 'auto' }}>
                {history.length === 0 && (
                  <small className="text-muted">No messages yet.</small>
                )}
                {history.map((h, i) => (
                  <div key={i} className="mb-2">
                    <small><strong>You:</strong> {h.query_text}</small>
                    <div><small><strong>Bot:</strong> {h.response_text}</small></div>
                  </div>
                ))}
              </div>

              <div className="input-group mt-2">
                <input 
                  className="form-control form-control-sm"
                  value={q}
                  onChange={e => setQ(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') ask(); }}
                  disabled={loading}
                  placeholder="Ask me something..."
                />
                <button 
                  className="btn btn-primary btn-sm" 
                  onClick={ask} 
                  disabled={loading}
                >
                  {loading ? '...' : 'Ask'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
