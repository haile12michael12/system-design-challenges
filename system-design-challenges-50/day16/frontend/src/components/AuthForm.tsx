import React from 'react'

interface AuthFormProps {
  username: string
  password: string
  setUsername: (username: string) => void
  setPassword: (password: string) => void
  onSubmit: (e: React.FormEvent) => void
  buttonText: string
}

const AuthForm: React.FC<AuthFormProps> = ({
  username,
  password,
  setUsername,
  setPassword,
  onSubmit,
  buttonText
}) => {
  return (
    <form onSubmit={onSubmit}>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">{buttonText}</button>
    </form>
  )
}

export default AuthForm