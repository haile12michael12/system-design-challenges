import React, { useState } from 'react'
import AuthForm from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'

const Signup: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')
  const { signup } = useAuth()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    signup(username, email, password)
  }

  return (
    <div className="signup-page">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <AuthForm
          username={username}
          password={password}
          setUsername={setUsername}
          setPassword={setPassword}
          onSubmit={handleSubmit}
          buttonText="Sign Up"
        />
      </form>
    </div>
  )
}

export default Signup