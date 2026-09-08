import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Historico from './pages/Historico';
import Configuracoes from './pages/Configuracoes';
import { useEffect, useState } from 'react';

function App() {
  const [isConfigured, setIsConfigured] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const url = localStorage.getItem('API_BASE_URL');
    if (url) {
      setIsConfigured(true);
    }
    setLoading(false);
  }, []);

  if (loading) return null;

  return (
    <Router>
      <div className="app-container">
        {!isConfigured ? (
          <Configuracoes onSave={() => setIsConfigured(true)} />
        ) : (
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/historico" element={<Historico />} />
            <Route path="/configuracoes" element={<Configuracoes />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        )}
      </div>
    </Router>
  );
}

export default App;
