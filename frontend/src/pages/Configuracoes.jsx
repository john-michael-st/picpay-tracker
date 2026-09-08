import React, { useState } from 'react';
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
}
