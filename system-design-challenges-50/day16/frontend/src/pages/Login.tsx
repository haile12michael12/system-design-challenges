import React, { useState } from 'react'
import AuthForm from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'

const Login: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { login } = useAuth()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    login(username, password)
  }

  return (
    <div className="login-page">
      <h1>Login</h1>
      <AuthForm
        username={username}
        password={password}
        setUsername={setUsername}
        setPassword={setPassword}
        onSubmit={handleSubmit}
        buttonText="Login"
      />
    </div>
  )
}

export default Login