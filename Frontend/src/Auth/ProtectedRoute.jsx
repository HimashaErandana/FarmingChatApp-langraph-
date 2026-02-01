import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();

  /*
  No token → no access
  */
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return children;
}
