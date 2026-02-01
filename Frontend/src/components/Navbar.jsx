import { useNavigate } from "react-router-dom";
import { useAuth } from "../Auth/AuthContext";

const Navbar = () => {

  const {logout} = useAuth()
  const navigate = useNavigate()
  const handleLogout = () => {
    logout()
    navigate("/login")
  };

  return (
    <nav className="sticky top-0 z-50 bg-gradient-to-r from-emerald-900 to-emerald-800 shadow-md border-b border-emerald-700/30">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-12 items-center justify-between">
          
          {/* Logo Section - Left */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-green-500 shadow-md">
              {/* Leaf Icon */}
              <svg 
                className="w-4 h-4 text-white" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M13 10V3L4 14h7v7l9-11h-7z" 
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold bg-gradient-to-r from-emerald-300 via-green-300 to-emerald-200 bg-clip-text text-transparent">
                AgroGo
              </span>
              <span className="text-[10px] text-emerald-300/80 font-medium tracking-wider leading-tight">
                Smart Farming
              </span>
            </div>
          </div>

          {/* Logout Button - Right */}
          <div className="flex items-center">
            <button
              onClick={handleLogout}
              className="group relative flex items-center space-x-2 px-3 py-1.5 rounded-md bg-gradient-to-r from-emerald-700/20 to-emerald-600/20 hover:from-emerald-600/30 hover:to-emerald-500/30 backdrop-blur-sm border border-emerald-600/30 hover:border-emerald-500/50 transition-all duration-200 hover:shadow-md hover:shadow-emerald-500/10"
            >
              {/* Glow effect */}
              <div className="absolute inset-0 rounded-md bg-gradient-to-r from-emerald-400/0 via-emerald-400/10 to-emerald-400/0 blur group-hover:via-emerald-400/20 transition-all duration-300" />
              
              {/* Logout Icon */}
              <svg 
                className="w-4 h-4 text-emerald-300 group-hover:text-emerald-200 transition-colors duration-200" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" 
                />
              </svg>
              
              <span className="text-xs font-medium text-emerald-100 group-hover:text-white transition-colors duration-200">
                Logout
              </span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;