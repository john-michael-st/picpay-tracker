import React from 'react';

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
}
