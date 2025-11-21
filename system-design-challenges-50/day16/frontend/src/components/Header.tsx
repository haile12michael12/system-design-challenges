import React from 'react'
import { useAuth } from '../hooks/useAuth'

const Header: React.FC = () => {
  const { user, logout } = useAuth()

  return (
    <header className="app-header">
      <div className="header-content">
        <h1>Authentication Service</h1>
        {user && (
          <div className="user-info">
            <span>Welcome, {user.username}!</span>
            <button onClick={logout}>Logout</button>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header