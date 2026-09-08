import React, { useState } from 'react';
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
}
