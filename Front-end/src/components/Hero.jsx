import React from 'react';

export const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-content">
        <p className="eyebrow">AI-NATIVE INFRASTRUCTURE PLATFORM</p>
        <h1>
          Ship production-ready AI
          <span className="accent"> in days, not months.</span>
        </h1>
        <p className="subtitle">
          NovaStack Labs gives your team a secure, scalable foundation for building chatbots,
          agents, and data products without wrestling with infra. Focus on prompts, not plumbing.
        </p>
        <div className="hero-actions">
          <button className="btn primary">Start free workspace</button>
          <button className="btn outline">Talk to an engineer</button>
        </div>
        <p className="hero-meta">
          Trusted by fast-moving teams at modern SaaS, fintech, and data companies.
        </p>
      </div>
      <div className="hero-panel">
        <div className="hero-card">
          <p className="hero-card-label">Realtime observability</p>
          <p className="hero-card-metric">99.99%</p>
          <p className="hero-card-caption">Uptime across all AI workloads this quarter.</p>
        </div>
        <div className="hero-card secondary">
          <p className="hero-card-label">Average deployment time</p>
          <p className="hero-card-metric">7.3 min</p>
          <p className="hero-card-caption">From Git push to live, auto-scaled endpoint.</p>
        </div>
      </div>
    </section>
  );
};


