import { useState, useEffect } from 'react';
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
}
