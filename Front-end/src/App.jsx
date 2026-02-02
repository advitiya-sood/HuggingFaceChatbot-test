import React from 'react';
import { NavBar } from './components/NavBar';
import { Hero } from './components/Hero';
import { Features } from './components/Features';
import { Solutions } from './components/Solutions';
import { Testimonials } from './components/Testimonials';
import { CTASection } from './components/CTASection';
import { Footer } from './components/Footer';
import ChatWidget from './components/ChatWidget';

function App() {
  return (
    <div className="app">
      <NavBar />
      <main>
        <Hero />
        <Features />
        <Solutions />
        <Testimonials />
        <CTASection />
      </main>
      <Footer />
      {/* Example visual placeholder for your chat widget. You can remove this when your real widget renders here. */}
      <div className="chat-widget-placeholder">
        <span className="dot" />
        <ChatWidget/>
      </div>
    </div>
  );
}

export default App;


