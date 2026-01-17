import React, { useState } from 'react';
import { LoginPage } from './pages/LoginPage';
import { Dashboard } from './pages/Dashboard';
import './styles/index.css';

function App() {
  const [username, setUsername] = useState<string | null>(localStorage.getItem('username'));

  const handleLogin = (user: string) => {
    setUsername(user);
    localStorage.setItem('username', user);
  };

  const handleLogout = () => {
    setUsername(null);
    localStorage.removeItem('username');
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      {username ? (
        <Dashboard username={username} onLogout={handleLogout} />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
