// src/api.js

const getBaseUrl = () => localStorage.getItem('API_BASE_URL') || '';
const getToken = () => localStorage.getItem('API_SECRET_TOKEN') || '';

/**
 * Headers padrão para todas as requisições.
 * Usa X-Token conforme o backend FastAPI espera.
 */
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-Token': getToken()
});

// Mock em caso de backend indisponível / offline
const getMockResumo = () => ({
  total_mes: 320.50,
  teto_normal: 300,
  teto_emergencial: 500,
  zona: 'laranja',
  percentual_normal: 100,
  percentual_emergencial: 10.25,
  restante_normal: 0,
  restante_emergencial: 179.50,
  mensagem_alerta: 'Teto atingido — consumindo reserva emergencial',
  gastos_por_categoria: {
    Alimentacao: 150.00,
    Assinaturas: 50.00,
    Transporte: 80.00,
    Saude: 0,
    Lazer: 40.50,
    Outros: 0
  }
});

export const getResumo = async () => {
  try {
    const res = await fetch(`${getBaseUrl()}/resumo`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erro ao buscar resumo');
    return await res.json();
  } catch (error) {
    console.warn('[PicPay Tracker] Backend indisponivel - usando dados de demonstracao.', error);
    return getMockResumo();
  }
};

export const getHistorico = async (mes, ano) => {
  try {
    const res = await fetch(`${getBaseUrl()}/historico?mes=${mes}&ano=${ano}`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erro ao buscar historico');
    return await res.json();
  } catch (error) {
    console.warn('[PicPay Tracker] Historico indisponivel.', error);
    return [];
  }
};

export const addGasto = async (descricao, valor) => {
  const valorFormatado = Number(valor).toFixed(2).replace('.', ',');
  const notificacao = `Lancamento manual: R$ ${valorFormatado} em ${descricao}`;
  const res = await fetch(`${getBaseUrl()}/gasto`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ notificacao, token: getToken() })
  });
  if (!res.ok) throw new Error('Erro ao adicionar gasto');
  return await res.json();
};

export const deleteGasto = async (id) => {
  const res = await fetch(`${getBaseUrl()}/gasto/${id}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Erro ao excluir gasto');
  return await res.json();
};

export const healthCheck = async (url, token) => {
  const res = await fetch(`${url}/health`, {
    headers: { 'Content-Type': 'application/json', 'X-Token': token }
  });
  if (!res.ok) throw new Error('Falha no health check');
  return await res.json();
};
