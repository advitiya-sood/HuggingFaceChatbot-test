# NovaStack Labs – Sample Tech Company Site

This is a small React + Vite frontend that mimics a modern AI/infra tech company landing page.  
It is designed as a simple playground where you can embed and test your **chat widget**.

## Running locally

1. Install dependencies:
   ```bash
   cd /Users/Advitiya.sood/Desktop/AI-chatbot/Front-end
   npm install
   ```

2. Start the dev server:
   ```bash
   npm run dev
   ```

3. Open the URL printed in the terminal (usually `http://localhost:5173`).

## Chat widget integration

There are **two convenient ways** to attach your widget:

1. **Mount into a dedicated DOM node**

   The root `index.html` includes an extra container:

   ```html
   <div id="chat-widget-container"></div>
   ```

   In your widget bootstrap code (for example, in a script tag or a small SDK), you can mount into this element:

   ```js
   const container = document.getElementById('chat-widget-container');
   if (container) {
     // Replace this with your actual widget mount call
     container.innerHTML = '<div>Your chat widget goes here</div>';
   }
   ```

2. **Replace the floating placeholder component**

   The `App.jsx` file includes a small visual hint of where a chat bubble typically sits:

   ```jsx
   <div className="chat-widget-placeholder">
     <span className="dot" />
     <span>Chat widget will appear here</span>
   </div>
   ```

   You can:
   - Remove this block entirely and let your real widget render as a floating bubble, or
   - Replace its contents with your widget component or snippet.

## Files to look at

- `src/App.jsx` – main layout and where the chat placeholder lives.
- `index.html` – contains the `#root` React mount point and `#chat-widget-container` for your widget.
- `src/styles.css` – page styling (dark, modern, responsive).


