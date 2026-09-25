import { createContext, useContext, useState, useCallback } from "react";
import { getUser, setSession as persistSession, clearSession as clearPersistedSession } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getUser());

  const login = useCallback((token, userData) => {
    persistSession(token, userData);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    clearPersistedSession();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
