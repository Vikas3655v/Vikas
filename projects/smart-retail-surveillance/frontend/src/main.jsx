import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${API}/api/analytics`)
      .then((response) => {
        if (!response.ok) throw new Error('Analytics API unavailable');
        return response.json();
      })
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <main className="shell"><h1>Smart Retail Analytics</h1><p className="error">{error}</p><p>Start the Python API and refresh the dashboard.</p></main>;
  if (!data) return <main className="shell"><h1>Smart Retail Analytics</h1><p>Loading analytics…</p></main>;

  const categories = Object.entries(data.categories || {});

  return (
    <main className="shell">
      <header><div><p className="eyebrow">AI-powered retail intelligence</p><h1>Smart Retail Analytics</h1><p className="muted">Aggregate, explainable insights from object-detection events.</p></div><span className="status">API Connected</span></header>
      <section className="metrics">
        <article><span>Detection events</span><strong>{data.total_events}</strong></article>
        <article><span>Unique categories</span><strong>{data.unique_categories}</strong></article>
        <article><span>Avg. confidence</span><strong>{data.average_confidence == null ? '—' : `${(data.average_confidence * 100).toFixed(1)}%`}</strong></article>
      </section>
      <section className="grid">
        <article className="card"><h2>Observed categories</h2>{categories.length ? categories.map(([name, count]) => <div className="row" key={name}><span>{name}</span><b>{count}</b></div>) : <p>No detection events found.</p>}</article>
        <article className="card"><h2>Recommendations</h2>{data.recommendations?.length ? data.recommendations.map((item) => <div className="recommendation" key={item.observed_category}><strong>{item.observed_category}</strong><p>{item.recommendation}</p><small>{item.observations} observations · {item.reason}</small></div>) : <p>No recommendation rules matched.</p>}</article>
      </section>
      <footer>Privacy-first design: event-level analytics only; no identity or biometric inference.</footer>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
