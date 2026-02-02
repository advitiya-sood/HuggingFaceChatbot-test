import React from 'react';

export const CTASection = () => {
  return (
    <section id="cta" className="section cta-section">
      <div className="cta-inner">
        <div>
          <h2>Ready to test your chat widget in production-like conditions?</h2>
          <p>
            Spin up a sandbox workspace, connect your models, and plug your widget into this page
            in minutes. No infra tickets required.
          </p>
        </div>
        <div className="cta-actions">
          <button className="btn primary">Launch sandbox</button>
          <p className="cta-caption">No credit card required. 14-day free trial.</p>
        </div>
      </div>
    </section>
  );
};


