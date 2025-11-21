import React from 'react'
import { useAuth } from '../hooks/useAuth'
import Header from '../components/Header'

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth()

  return (
    <div className="dashboard-page">
      <Header />
      <h1>Dashboard</h1>
      {user ? (
        <div>
          <p>Welcome, {user.username}!</p>
          <p>Email: {user.email}</p>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  )
}

export default Dashboard