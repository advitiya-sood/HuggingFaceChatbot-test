import React from 'react';

const solutions = [
  {
    name: 'Customer support copilots',
    detail: 'Deflect tickets with AI agents that understand your product, docs, and policies.',
  },
  {
    name: 'Internal knowledge chat',
    detail: 'Give every team a secure assistant over Confluence, Notion, and Git repos.',
  },
  {
    name: 'Data & analytics assistants',
    detail: 'Let stakeholders ask questions in natural language while you keep governance in place.',
  },
];

export const Solutions = () => {
  return (
    <section id="solutions" className="section muted">
      <div className="section-header">
        <h2>Built for modern product and platform teams.</h2>
        <p>
          Whether you&apos;re shipping your first chatbot or running dozens of AI workloads, our
          platform adapts to your stack and compliance needs.
        </p>
      </div>
      <div className="grid three">
        {solutions.map((s) => (
          <div key={s.name} className="card solution-card">
            <h3>{s.name}</h3>
            <p>{s.detail}</p>
          </div>
        ))}
      </div>
    </section>
  );
};


