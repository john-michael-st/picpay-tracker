import React, { useState } from 'react';
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
}
