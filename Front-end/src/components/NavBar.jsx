import React from 'react';

export const NavBar = () => {
  return (
    <header className="nav">
      <div className="nav-left">
        <div className="logo-mark">N</div>
        <span className="logo-text">NovaStack Labs</span>
      </div>
      <nav className="nav-links">
        <a href="#features">Platform</a>
        <a href="#solutions">Solutions</a>
        <a href="#testimonials">Customers</a>
        <a href="#cta">Pricing</a>
      </nav>
      <div className="nav-actions">
        <button className="btn ghost">Log in</button>
        <button className="btn primary">Book demo</button>
      </div>
    </header>
  );
};


