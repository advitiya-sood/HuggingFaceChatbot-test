import React from 'react';

const items = [
  {
    title: 'Unified orchestration',
    body: 'Connect OpenAI, local models, vector stores, and your own APIs behind a single typed interface.',
  },
  {
    title: 'Enterprise-grade security',
    body: 'SOC2-ready controls, fine-grained roles, and full audit logs baked into every workflow.',
  },
  {
    title: 'Deep analytics',
    body: 'Trace every conversation, token, and latency spike with built-in dashboards and exports.',
  },
];

export const Features = () => {
  return (
    <section id="features" className="section">
      <div className="section-header">
        <h2>Everything you need to run AI in production.</h2>
        <p>
          From experimentation to compliant production workloads, NovaStack Labs centralizes the
          tools your team relies on to build resilient AI experiences.
        </p>
      </div>
      <div className="grid three">
        {items.map((item) => (
          <div key={item.title} className="card feature-card">
            <h3>{item.title}</h3>
            <p>{item.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
};


