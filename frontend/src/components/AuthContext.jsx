import { createContext, useContext, useEffect, useState } from "react";
import { useLocation } from 'react-router-dom';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const location = useLocation();

  const login = () => setIsAuthenticated(true);
  const logout = () => setIsAuthenticated(false);

  const checkAuth = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/session`, {
        credentials: 'include',
      });
      const data = await response.json();

      setIsAuthenticated(data.logged_in); // API powinno to zwrócić
    } catch {
      setIsAuthenticated(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    checkAuth(); 
  }, [location.pathname]);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export { AuthContext };