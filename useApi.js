import { useEffect, useState } from "react";

function useApi(requestFn, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const run = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await requestFn();
      setData(response.data);
    } catch (err) {
      setError(err.message || "Error al cargar datos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    run();
  }, dependencies);

  return {
    data,
    loading,
    error,
    refetch: run,
  };
}

export default useApi;
