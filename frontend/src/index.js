import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Global styles
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

// Get root container
const container = document.getElementById('root');
const root = createRoot(container);

// Render app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
