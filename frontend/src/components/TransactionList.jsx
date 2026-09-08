import React from 'react';
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
}
