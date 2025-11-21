import { useState, useEffect } from 'react'
import api from '../services/api'

interface User {
  id: number
  username: string
  email: string
}

interface AuthHook {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  signup: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
  handleToken: (token: string) => void
  requestPasswordReset: (email: string) => Promise<void>
  resetPassword: (token: string, newPassword: string) => Promise<void>
}

export const useAuth = (): AuthHook => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('access_token')
    if (token) {
      // In a real implementation, we would verify the token
      // and fetch user data from the server
    }
  }, [])

  const login = async (username: string, password: string) => {
    setLoading(true)
    try {
      const response = await api.post('/auth/login', { username, password })
      const { access_token, refresh_token } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      // Fetch user data
      // setUser(userData)
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const signup = async (username: string, email: string, password: string) => {
    setLoading(true)
    try {
      await api.post('/auth/register', { username, email, password })
    } catch (error) {
      console.error('Signup failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  const handleToken = (token: string) => {
    localStorage.setItem('access_token', token)
    // Fetch user data and set user
  }

  const requestPasswordReset = async (email: string) => {
    setLoading(true)
    try {
      await api.post('/auth/reset-password/request', { email })
    } catch (error) {
      console.error('Password reset request failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const resetPassword = async (token: string, newPassword: string) => {
    setLoading(true)
    try {
      await api.post('/auth/reset-password/confirm', { token, newPassword })
    } catch (error) {
      console.error('Password reset failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  return {
    user,
    loading,
    login,
    signup,
    logout,
    handleToken,
    requestPasswordReset,
    resetPassword
  }
}