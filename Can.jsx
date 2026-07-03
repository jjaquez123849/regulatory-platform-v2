import { useAuth } from "./AuthContext.jsx";

function Can({ permission, capability, children, fallback = null }) {
  const { hasPermission, hasCapability } = useAuth();

  if (permission && !hasPermission(permission)) {
    return fallback;
  }

  if (capability && !hasCapability(capability)) {
    return fallback;
  }

  return children;
}

export default Can;
