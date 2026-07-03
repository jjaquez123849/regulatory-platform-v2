import { Navigate } from "react-router-dom";

import LoadingState from "../../components/feedback/LoadingState.jsx";
import { useAuth } from "./AuthContext.jsx";

function ProtectedRoute({ children }) {
  const { loading, isAuthenticated } = useAuth();

  if (loading) {
    return <LoadingState message="Validando sesión..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
