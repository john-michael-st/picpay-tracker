import os
import json

base_dir = r"c:\Users\jm916\OneDrive\Documentos\picpay-tracker\frontend"

dirs = [
    "public",
    "src/components",
    "src/pages",
    "src/hooks",
    "src/styles"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {}

files["package.json"] = """{
  "name": "picpay-tracker-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.0",
    "vite-plugin-pwa": "^0.17.4"
  }
}"""

files["vite.config.js"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'PicPay Tracker',
        short_name: 'Tracker',
        start_url: '/',
        display: 'standalone',
        background_color: '#0f172a',
        theme_color: '#6366f1',
        icons: [
          { src: '/icon-192.svg', sizes: '192x192', type: 'image/svg+xml' },
          { src: '/icon-512.svg', sizes: '512x512', type: 'image/svg+xml' }
        ]
      }
    })
  ]
});"""

files["index.html"] = """<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/icon-192.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <meta name="theme-color" content="#0f172a" />
    <title>PicPay Tracker</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""

files["public/manifest.json"] = """{
  "name": "PicPay Tracker",
  "short_name": "Tracker",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0f172a",
  "theme_color": "#6366f1",
  "icons": [
    { "src": "/icon-192.svg", "sizes": "192x192", "type": "image/svg+xml" },
    { "src": "/icon-512.svg", "sizes": "512x512", "type": "image/svg+xml" }
  ]
}"""

svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#6366f1" rx="100"/>
  <text x="50%" y="50%" fill="#fff" font-size="250" font-family="sans-serif" font-weight="bold" text-anchor="middle" dy=".3em">$</text>
</svg>"""

files["public/icon-192.svg"] = svg_icon
files["public/icon-512.svg"] = svg_icon

files["src/main.jsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""

files["src/App.jsx"] = """import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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

export default App;"""

files["src/api.js"] = """// src/api.js
const getHeaders = () => {
  const token = localStorage.getItem('API_SECRET_TOKEN') || '';
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

const getBaseUrl = () => {
  return localStorage.getItem('API_BASE_URL') || '';
};

// Funções de mock em caso de backend indisponível / offline
const getMockResumo = () => ({
  gasto_total: 320.50,
  teto_normal: 300,
  reserva: 200,
  categorias: [
    { nome: 'Alimentação', icone: '🍔', gasto: 150.00 },
    { nome: 'Assinaturas', icone: '📱', gasto: 50.00 },
    { nome: 'Transporte', icone: '🚗', gasto: 80.00 },
    { nome: 'Saúde', icone: '🏥', gasto: 0.00 },
    { nome: 'Lazer', icone: '🎮', gasto: 40.50 },
    { nome: 'Outros', icone: '📦', gasto: 0.00 }
  ],
  ultimos_lancamentos: [
    { id: 1, categoria: 'Alimentação', icone: '🍔', descricao: 'Ifood', valor: 35.00, data: new Date().toISOString() }
  ]
});

export const getResumo = async () => {
  try {
    const res = await fetch(`${getBaseUrl()}/resumo`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erro ao buscar resumo');
    return await res.json();
  } catch (error) {
    console.warn("Retornando mock para getResumo", error);
    return getMockResumo();
  }
};

export const getHistorico = async (mes, ano) => {
  try {
    const res = await fetch(`${getBaseUrl()}/historico?mes=${mes}&ano=${ano}`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erro ao buscar historico');
    return await res.json();
  } catch (error) {
    console.warn("Retornando mock para getHistorico", error);
    return { gastos: [], total: 0 };
  }
};

export const addGasto = async (descricao, valor, categoria) => {
  const res = await fetch(`${getBaseUrl()}/gastos`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ descricao, valor, categoria })
  });
  if (!res.ok) throw new Error('Erro ao adicionar gasto');
  return await res.json();
};

export const deleteGasto = async (id) => {
  const res = await fetch(`${getBaseUrl()}/gastos/${id}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Erro ao excluir gasto');
  return await res.json();
};

export const healthCheck = async (url, token) => {
  const res = await fetch(`${url}/health`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });
  if (!res.ok) throw new Error('Falha no health check');
  return await res.json();
};"""

files["src/hooks/useResumo.js"] = """import { useState, useEffect } from 'react';
import { getResumo } from '../api';

export function useResumo() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchResumo = async () => {
    try {
      const result = await getResumo();
      setData(result);
      setError(null);
    } catch (err) {
      setError('Não foi possível carregar os dados. Você pode estar offline.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumo();
    const interval = setInterval(fetchResumo, 30000); // polling 30s
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error, refetch: fetchResumo };
}"""

files["src/styles/global.css"] = """:root {
  --bg-dark: #0f172a;
  --bg-card: #1e293b;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --accent: #6366f1;
  --accent-hover: #4f46e5;
  --color-green: #22c55e;
  --color-yellow: #eab308;
  --color-orange: #f97316;
  --color-red: #ef4444;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

body {
  background-color: var(--bg-dark);
  color: var(--text-main);
  -webkit-font-smoothing: antialiased;
}

.app-container {
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
  background-color: var(--bg-dark);
  padding-bottom: 80px;
}

/* Headers */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.header h1 {
  font-size: 1.25rem;
  font-weight: 600;
}

.icon-button {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
}

/* Dashboard Layout */
.dashboard-content {
  padding: 0 20px;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 24px 0 12px;
}

/* Velocimetro */
.velocimetro-container {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.progress-bar-wrapper {
  height: 20px;
  background: #334155;
  border-radius: 10px;
  overflow: hidden;
  margin: 16px 0;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease-in-out, background-color 0.5s ease;
}

.velocimetro-value {
  font-size: 2rem;
  font-weight: 700;
}

.velocimetro-legend {
  font-size: 0.875rem;
  color: var(--text-muted);
}

/* Category Cards */
.category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.category-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-card.empty .cat-value {
  color: var(--text-muted);
}

.cat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.cat-value {
  font-size: 1.125rem;
  font-weight: 600;
}

/* Transaction List */
.transaction-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.transaction-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-card);
  padding: 12px 16px;
  border-radius: 12px;
}

.transaction-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.transaction-icon {
  font-size: 1.5rem;
}

.transaction-desc {
  font-weight: 500;
  font-size: 0.95rem;
}

.transaction-date {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.transaction-amount {
  font-weight: 600;
}

/* FAB */
.fab {
  position: fixed;
  bottom: 24px;
  right: max(24px, calc(50% - 216px));
  width: 56px;
  height: 56px;
  border-radius: 28px;
  background: var(--accent);
  color: white;
  border: none;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  cursor: pointer;
  z-index: 100;
}

/* Modals & Forms */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 200;
}

.modal-content {
  background: var(--bg-card);
  width: 100%;
  max-width: 480px;
  border-radius: 24px 24px 0 0;
  padding: 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.form-control {
  width: 100%;
  background: var(--bg-dark);
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 12px;
  color: white;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: var(--accent);
}

.btn-primary {
  width: 100%;
  background: var(--accent);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-secondary {
  width: 100%;
  background: #334155;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 12px;
}

/* Configuracoes */
.config-page {
  padding: 20px;
}

.alert-banner {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: 500;
  text-align: center;
}
.alert-success { background: rgba(34, 197, 94, 0.2); color: var(--color-green); }
.alert-error { background: rgba(239, 68, 68, 0.2); color: var(--color-red); }

/* Utility colors */
.text-green { color: var(--color-green); }
.text-yellow { color: var(--color-yellow); }
.text-orange { color: var(--color-orange); }
.text-red { color: var(--color-red); }
"""

files["src/components/Velocimetro.jsx"] = """import React from 'react';

export default function Velocimetro({ gastoTotal, tetoNormal, reserva }) {
  const totalDisponivel = tetoNormal + reserva;
  const percentual = Math.min((gastoTotal / totalDisponivel) * 100, 100);
  
  let zonaClass = 'text-green';
  let barraColor = 'var(--color-green)';

  // Corrigindo regra de cor conforme prompt
  // 🟢 Verde: R$ 0 a R$ 250 (seguro)
  // 🟡 Amarela: R$ 251 a R$ 300 (atenção)
  // 🟠 Laranja: R$ 301 a R$ 500 (emergência)
  // 🔴 Vermelha: acima de R$ 500 (crítico)
  if (gastoTotal <= 250) {
    zonaClass = 'text-green'; barraColor = 'var(--color-green)';
  } else if (gastoTotal <= 300) {
    zonaClass = 'text-yellow'; barraColor = 'var(--color-yellow)';
  } else if (gastoTotal <= 500) {
    zonaClass = 'text-orange'; barraColor = 'var(--color-orange)';
  } else {
    zonaClass = 'text-red'; barraColor = 'var(--color-red)';
  }

  const formatBRL = (val) => val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

  return (
    <div className="velocimetro-container">
      <div className={`velocimetro-value ${zonaClass}`}>
        {formatBRL(gastoTotal)}
      </div>
      
      <div className="progress-bar-wrapper">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentual}%`, backgroundColor: barraColor }}
        ></div>
      </div>

      <div className="velocimetro-legend">
        Teto normal: {formatBRL(tetoNormal)} | Reserva: {formatBRL(reserva)}
      </div>
      
      {gastoTotal > tetoNormal && (
        <div className="text-orange" style={{ fontSize: '0.875rem', marginTop: '8px' }}>
          ⚠️ Usando reserva: {formatBRL(gastoTotal - tetoNormal)}
        </div>
      )}
    </div>
  );
}"""

files["src/components/CategoryCard.jsx"] = """import React from 'react';

export default function CategoryCard({ nome, icone, gasto }) {
  const isZero = gasto === 0;
  
  return (
    <div className={`category-card ${isZero ? 'empty' : ''}`}>
      <div className="cat-header">
        <span>{icone}</span>
        <span>{nome}</span>
      </div>
      <div className="cat-value">
        {gasto.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
      </div>
    </div>
  );
}"""

files["src/components/TransactionList.jsx"] = """import React from 'react';
import TransactionItem from './TransactionItem';

export default function TransactionList({ transactions, onDelete }) {
  if (!transactions || transactions.length === 0) {
    return <p style={{ color: 'var(--text-muted)' }}>Nenhum lançamento encontrado.</p>;
  }

  return (
    <div className="transaction-list">
      {transactions.map(t => (
        <TransactionItem key={t.id} transaction={t} onDelete={onDelete} />
      ))}
    </div>
  );
}"""

files["src/components/TransactionItem.jsx"] = """import React from 'react';

export default function TransactionItem({ transaction, onDelete }) {
  const { icone, descricao, valor, data } = transaction;

  // Define a cor com base no valor ou na zona. Aqui simplificaremos.
  const formatBRL = (val) => val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  
  const formatDate = (isoStr) => {
    const d = new Date(isoStr);
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  };

  return (
    <div className="transaction-item">
      <div className="transaction-info">
        <div className="transaction-icon">{icone || '🛒'}</div>
        <div>
          <div className="transaction-desc">{descricao}</div>
          <div className="transaction-date">{formatDate(data)}</div>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div className="transaction-amount">
          {formatBRL(valor)}
        </div>
        {onDelete && (
          <button onClick={() => onDelete(transaction.id)} style={{ background: 'none', border: 'none', color: 'var(--color-red)', cursor: 'pointer', fontSize: '1.25rem' }}>
            ✕
          </button>
        )}
      </div>
    </div>
  );
}"""

files["src/components/AddExpenseModal.jsx"] = """import React, { useState } from 'react';
import { addGasto } from '../api';

export default function AddExpenseModal({ onClose, onSuccess }) {
  const [descricao, setDescricao] = useState('');
  const [valor, setValor] = useState('');
  const [categoria, setCategoria] = useState('Alimentação');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await addGasto(descricao, parseFloat(valor.replace(',', '.')), categoria);
      onSuccess();
      onClose();
    } catch (err) {
      alert("Erro ao salvar: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2 className="modal-title">Novo Lançamento</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Descrição</label>
            <input 
              type="text" 
              className="form-control" 
              required 
              value={descricao}
              onChange={e => setDescricao(e.target.value)}
              placeholder="Ex: Almoço Ifood"
            />
          </div>
          <div className="form-group">
            <label>Valor (R$)</label>
            <input 
              type="number" 
              step="0.01"
              className="form-control" 
              required 
              value={valor}
              onChange={e => setValor(e.target.value)}
              placeholder="0.00"
            />
          </div>
          <div className="form-group">
            <label>Categoria</label>
            <select className="form-control" value={categoria} onChange={e => setCategoria(e.target.value)}>
              <option value="Alimentação">Alimentação</option>
              <option value="Assinaturas">Assinaturas</option>
              <option value="Transporte">Transporte</option>
              <option value="Saúde">Saúde</option>
              <option value="Lazer">Lazer</option>
              <option value="Outros">Outros</option>
            </select>
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Salvando...' : 'Salvar Gasto'}
          </button>
        </form>
      </div>
    </div>
  );
}"""

files["src/pages/Dashboard.jsx"] = """import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useResumo } from '../hooks/useResumo';
import Velocimetro from '../components/Velocimetro';
import CategoryCard from '../components/CategoryCard';
import TransactionList from '../components/TransactionList';
import AddExpenseModal from '../components/AddExpenseModal';

export default function Dashboard() {
  const navigate = useNavigate();
  const { data, loading, error, refetch } = useResumo();
  const [showModal, setShowModal] = useState(false);

  const monthName = new Date().toLocaleString('pt-BR', { month: 'long', year: 'numeric' });
  const formattedMonth = monthName.charAt(0).toUpperCase() + monthName.slice(1);

  if (loading) return <div style={{ padding: 20 }}>Carregando...</div>;
  if (error && !data) return <div style={{ padding: 20 }}>Erro: {error}</div>;

  const resumo = data || { gasto_total: 0, teto_normal: 300, reserva: 200, categorias: [], ultimos_lancamentos: [] };

  return (
    <>
      <header className="header">
        <h1>{formattedMonth}</h1>
        <button className="icon-button" onClick={() => navigate('/configuracoes')}>⚙️</button>
      </header>

      <main className="dashboard-content">
        <Velocimetro 
          gastoTotal={resumo.gasto_total} 
          tetoNormal={resumo.teto_normal} 
          reserva={resumo.reserva} 
        />

        <h2 className="section-title">Categorias</h2>
        <div className="category-grid">
          {resumo.categorias.map(c => (
            <CategoryCard key={c.nome} nome={c.nome} icone={c.icone} gasto={c.gasto} />
          ))}
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 24, marginBottom: 12 }}>
          <h2 className="section-title" style={{ margin: 0 }}>Últimos Lançamentos</h2>
          <button onClick={() => navigate('/historico')} style={{ background: 'none', border: 'none', color: 'var(--accent)', cursor: 'pointer', fontWeight: 600 }}>Ver todos</button>
        </div>
        <TransactionList transactions={resumo.ultimos_lancamentos} />
      </main>

      <button className="fab" onClick={() => setShowModal(true)}>+</button>

      {showModal && (
        <AddExpenseModal onClose={() => setShowModal(false)} onSuccess={refetch} />
      )}
    </>
  );
}"""

files["src/pages/Historico.jsx"] = """import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistorico, deleteGasto } from '../api';
import TransactionList from '../components/TransactionList';

export default function Historico() {
  const navigate = useNavigate();
  const [gastos, setGastos] = useState([]);
  const [total, setTotal] = useState(0);
  const [mes, setMes] = useState(new Date().getMonth() + 1);
  const [ano, setAno] = useState(new Date().getFullYear());

  const fetchDados = async () => {
    try {
      const data = await getHistorico(mes, ano);
      setGastos(data.gastos || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDados();
  }, [mes, ano]);

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este gasto?')) {
      try {
        await deleteGasto(id);
        fetchDados();
      } catch (err) {
        alert("Erro ao excluir: " + err.message);
      }
    }
  };

  return (
    <div>
      <header className="header">
        <button className="icon-button" onClick={() => navigate('/')}>←</button>
        <h1>Histórico</h1>
        <div style={{ width: 24 }}></div>
      </header>

      <main className="dashboard-content">
        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
          <select className="form-control" value={mes} onChange={e => setMes(parseInt(e.target.value))}>
            {Array.from({length: 12}).map((_, i) => (
              <option key={i+1} value={i+1}>{new Date(0, i).toLocaleString('pt-BR', {month: 'long'})}</option>
            ))}
          </select>
          <select className="form-control" value={ano} onChange={e => setAno(parseInt(e.target.value))}>
            {[2024, 2025, 2026, 2027].map(a => <option key={a} value={a}>{a}</option>)}
          </select>
        </div>

        <div className="velocimetro-container" style={{ marginBottom: '24px' }}>
          <div className="velocimetro-legend">Total no mês</div>
          <div className="velocimetro-value text-main">
            {total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </div>
        </div>

        <TransactionList transactions={gastos} onDelete={handleDelete} />
      </main>
    </div>
  );
}"""

files["src/pages/Configuracoes.jsx"] = """import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { healthCheck } from '../api';

export default function Configuracoes({ onSave }) {
  const navigate = useNavigate();
  const [url, setUrl] = useState(localStorage.getItem('API_BASE_URL') || '');
  const [token, setToken] = useState(localStorage.getItem('API_SECRET_TOKEN') || '');
  const [status, setStatus] = useState(null);

  const handleTest = async () => {
    try {
      setStatus('Testando...');
      await healthCheck(url, token);
      setStatus({ type: 'success', msg: 'Conexão bem sucedida!' });
    } catch (err) {
      setStatus({ type: 'error', msg: 'Falha na conexão: ' + err.message });
    }
  };

  const handleSave = () => {
    localStorage.setItem('API_BASE_URL', url);
    localStorage.setItem('API_SECRET_TOKEN', token);
    if (onSave) onSave();
    else navigate('/');
  };

  return (
    <div className="config-page">
      {!onSave && (
        <header className="header" style={{ padding: '0 0 20px' }}>
          <button className="icon-button" onClick={() => navigate('/')}>←</button>
          <h1>Configurações</h1>
          <div style={{ width: 24 }}></div>
        </header>
      )}

      {onSave && (
        <div style={{ textAlign: 'center', marginBottom: 32, marginTop: 40 }}>
          <div style={{ fontSize: '3rem', marginBottom: 16 }}>👋</div>
          <h2>Bem-vindo ao Tracker</h2>
          <p style={{ color: 'var(--text-muted)' }}>Configure seu backend para começar.</p>
        </div>
      )}

      {status && status.type && (
        <div className={`alert-banner alert-${status.type}`}>
          {status.msg}
        </div>
      )}

      <div className="form-group">
        <label>URL do Backend</label>
        <input 
          type="url" 
          className="form-control" 
          value={url} 
          onChange={e => setUrl(e.target.value)} 
          placeholder="https://sua-api.vercel.app"
        />
      </div>

      <div className="form-group">
        <label>Secret Token</label>
        <input 
          type="password" 
          className="form-control" 
          value={token} 
          onChange={e => setToken(e.target.value)} 
          placeholder="Seu token secreto"
        />
      </div>

      <button className="btn-secondary" onClick={handleTest}>Testar Conexão</button>
      <button className="btn-primary" style={{ marginTop: 16 }} onClick={handleSave}>Salvar e Continuar</button>
      
      <div style={{ marginTop: 40, textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
        PicPay Tracker v1.0.0 <br/>
        Frontend PWA
      </div>
    </div>
  );
}"""

files["README_FRONTEND.md"] = """# PicPay Tracker - Frontend

Este é o frontend PWA do aplicativo PicPay Tracker, desenvolvido em React + Vite.

## Como instalar e rodar localmente

1. Certifique-se de ter o Node.js instalado (v18+).
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Rode o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
4. Acesse `http://localhost:5173` no navegador.

## Como fazer o deploy na Vercel

1. Crie uma conta no [Vercel](https://vercel.com).
2. Você pode conectar seu repositório GitHub e importar o projeto, escolhendo a pasta `frontend`. O Vercel detectará automaticamente que é um app Vite.
3. **Alternativa Manual (Drag & Drop):**
   - Rode `npm run build` localmente para gerar a pasta `dist/`.
   - Arraste a pasta `dist/` gerada para a página principal da sua dashboard no Vercel.

## Decisões Técnicas

- **PWA**: Utilizado o plugin `vite-plugin-pwa` para gerar automaticamente o Service Worker e manifest.json. O app é instalável e guarda cache local de forma básica para ser aberto offline.
- **Armazenamento de Configurações**: URL da API e Token são salvos no `localStorage` do dispositivo. Isso facilita o deploy do frontend (não precisa de .env no build) e permite usar a mesma interface conectando a backends diferentes, caso desejado.
- **Estilização**: Uso de CSS Vanilla com Variáveis (CSS Variables) seguindo um padrão mobile-first. Permite manter o pacote enxuto sem depender de bibliotecas de UI pesadas (Tailwind, MUI), garantindo um carregamento mais rápido no PWA.
- **Hooks customizados**: `useResumo.js` foi criado para implementar um polling (30s) que atualiza os dados na tela Dashboard automaticamente.
"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffold complete.")
