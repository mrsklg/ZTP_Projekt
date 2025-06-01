import { Navigate, Outlet } from 'react-router';
import { useAuth } from './AuthContext';

export default function PrivateRoute() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated === false) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
