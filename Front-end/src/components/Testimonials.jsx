import React from 'react';

const quotes = [
  {
    company: 'LinearFlow',
    quote:
      'We embedded NovaStack Labs into our infra in a week and cut our AI infra incidents by 60%.',
    name: 'Maya Chen',
    role: 'Head of Platform',
  },
  {
    company: 'Northwind Finance',
    quote:
      'Their observability dashboard is the first thing I check every morning. It just works.',
    name: 'David Kim',
    role: 'VP Engineering',
  },
];

export const Testimonials = () => {
  return (
    <section id="testimonials" className="section">
      <div className="section-header">
        <h2>Teams ship faster with NovaStack Labs.</h2>
        <p>Used in production by high-growth SaaS, fintech, and data companies worldwide.</p>
      </div>
      <div className="grid two">
        {quotes.map((q) => (
          <figure key={q.company} className="card testimonial-card">
            <blockquote>“{q.quote}”</blockquote>
            <figcaption>
              <span className="testimonial-name">{q.name}</span>
              <span className="testimonial-meta">
                {q.role}, {q.company}
              </span>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
};


