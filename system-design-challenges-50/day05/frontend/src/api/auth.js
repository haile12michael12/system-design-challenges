// Authentication API client
import apiClient from './index'

export const authApi = {
  // Login
  login(credentials) {
    return apiClient.post('/auth/login', credentials)
  },

  // Register
  register(userData) {
    return apiClient.post('/auth/register', userData)
  },

  // Logout
  logout() {
    return apiClient.post('/auth/logout')
  }
}