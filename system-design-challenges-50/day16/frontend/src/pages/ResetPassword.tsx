import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'

const ResetPassword: React.FC = () => {
  const [email, setEmail] = useState('')
  const [token, setToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [step, setStep] = useState<'request' | 'reset'>('request')
  const { requestPasswordReset, resetPassword } = useAuth()

  const handleRequest = (e: React.FormEvent) => {
    e.preventDefault()
    requestPasswordReset(email)
    setStep('reset')
  }

  const handleReset = (e: React.FormEvent) => {
    e.preventDefault()
    resetPassword(token, newPassword)
  }

  return (
    <div className="reset-password-page">
      <h1>Reset Password</h1>
      {step === 'request' ? (
        <form onSubmit={handleRequest}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit">Send Reset Link</button>
        </form>
      ) : (
        <form onSubmit={handleReset}>
          <input
            type="text"
            placeholder="Reset Token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <button type="submit">Reset Password</button>
        </form>
      )}
    </div>
  )
}

export default ResetPassword