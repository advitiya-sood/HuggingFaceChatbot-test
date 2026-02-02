import React from 'react';

export const Footer = () => {
  return (
    <footer className="footer">
      <span>© {new Date().getFullYear()} NovaStack Labs.</span>
      <div className="footer-links">
        <a href="#features">Docs</a>
        <a href="#solutions">Changelog</a>
        <a href="#cta">Security</a>
      </div>
    </footer>
  );
};


