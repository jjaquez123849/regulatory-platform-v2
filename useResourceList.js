import { useEffect, useState } from "react";

function useResourceList(listFn, params = {}, dependencies = []) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await listFn(params);
      setData(response.data || []);
    } catch (err) {
      setError(err.message || "Error al cargar datos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, dependencies);

  return {
    data,
    loading,
    error,
    refetch: load,
    setData,
  };
}

export default useResourceList;
