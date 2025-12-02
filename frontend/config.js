// Konfiguration für BrainPlan_LLM Frontend
// Diese Datei kann angepasst werden, um zwischen Mock-Daten und echtem Backend zu wechseln

// Setzen Sie USE_MOCK_DATA auf false, um das echte Backend zu verwenden
window.USE_MOCK_DATA = true;

// Setzen Sie die Backend-URL (wird nur verwendet, wenn USE_MOCK_DATA = false)
window.BACKEND_URL = 'http://localhost:5000';

// Für Production-Deployment (GitHub Pages mit separatem Backend):
// window.USE_MOCK_DATA = false;
// window.BACKEND_URL = 'https://your-backend-domain.com';
