import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css'; // We will create this next

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! Ask me anything about SMIK.", sender: "bot" }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  // Auto-scroll to bottom when messages change
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // 1. Add User Message
    const userMessage = { text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      // 2. Call your Python Backend (Render URL)
      // REPLACE with your actual Render URL
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.text }),
      });

      const data = await response.json();

      // 3. Add AI Response
      setMessages((prev) => [...prev, { text: data.answer, sender: "bot" }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev, 
        { text: "I'm waking up! Please try again in 10s.", sender: "bot" }
      ]);
      // Optional: Ping health endpoint
      fetch("https://your-app-name.onrender.com/health");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSendMessage();
  };

  return (
    <>
      {/* Floating Button */}
      <button className="chat-btn" onClick={toggleChat}>
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chat Box */}
      {isOpen && (
        <div className="chat-box">
          <div className="chat-header">
            SMIK Assistant
            <span className="close-btn" onClick={toggleChat}>✕</span>
          </div>
          
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`msg ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            {isLoading && <div className="msg loading">Thinking...</div>}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type a message..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;