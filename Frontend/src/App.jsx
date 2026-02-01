import './App.css'
import Login from './pages/Login'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Chat from './pages/chat';
import ProtectedRoute from './Auth/ProtectedRoute';
import { AuthProvider } from './Auth/AuthContext';
import Signup from './pages/Signup';


function App() {
  

  return (
    
   <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />  
          
          <Route
            path="/Chat/:uid"
            element={
              <ProtectedRoute>
                <Chat />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>

  )
}

export default App
