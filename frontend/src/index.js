import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css"; // Import your global styles
import App from "./App"; // Import the main App component

// Render the App component into the root DOM node
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
