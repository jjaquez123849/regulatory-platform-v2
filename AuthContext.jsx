import { createContext, useContext, useEffect, useState } from "react";

import { me } from "./authApi";
import { getMyEffectiveAccess } from "../admin/iam/iamApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [effectiveAccess, setEffectiveAccess] = useState({
    roles: [],
    permissions: [],
    capabilities: [],
    teams: [],
  });
  const [loading, setLoading] = useState(true);

  const loadCurrentUser = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setCurrentUser(null);
      setLoading(false);
      return;
    }

    try {
      const [userResponse, accessResponse] = await Promise.all([
        me(),
        getMyEffectiveAccess(),
      ]);

      setCurrentUser(userResponse.data);
      setEffectiveAccess(accessResponse.data);
    } catch {
      localStorage.removeItem("access_token");
      setCurrentUser(null);
      setEffectiveAccess({
        roles: [],
        permissions: [],
        capabilities: [],
        teams: [],
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCurrentUser();
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    setCurrentUser(null);
    setEffectiveAccess({
      roles: [],
      permissions: [],
      capabilities: [],
      teams: [],
    });
  };

  const hasPermission = (permission) => {
    return (
      effectiveAccess.permissions?.includes("*") ||
      effectiveAccess.permissions?.includes(permission)
    );
  };

  const hasCapability = (capability) => {
    return (
      effectiveAccess.capabilities?.includes("*") ||
      effectiveAccess.capabilities?.includes(capability)
    );
  };

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        effectiveAccess,
        loading,
        isAuthenticated: Boolean(currentUser),
        refreshUser: loadCurrentUser,
        logout,
        hasPermission,
        hasCapability,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
