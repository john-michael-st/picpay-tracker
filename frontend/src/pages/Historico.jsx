import React, { useState, useEffect } from 'react';
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
}
