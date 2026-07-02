import { useState } from "react";

function useAsyncAction() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const run = async (actionFn) => {
    try {
      setLoading(true);
      setError("");

      return await actionFn();
    } catch (err) {
      setError(err.message || "Error ejecutando acción");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    run,
  };
}

export default useAsyncAction;
