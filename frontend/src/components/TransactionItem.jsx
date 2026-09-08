import React from 'react';

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
}
