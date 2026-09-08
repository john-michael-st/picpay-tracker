import React from 'react';

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
}
