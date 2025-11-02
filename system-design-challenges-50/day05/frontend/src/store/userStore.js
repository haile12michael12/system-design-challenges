// User store module
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),
  
  getters: {
    getUser: (state) => state.user,
    getIsAuthenticated: (state) => state.isAuthenticated
  },
  
  actions: {
    setUser(user) {
      this.user = user
      this.isAuthenticated = true
    },
    
    logout() {
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('access_token')
    },
    
    async login(credentials) {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // For demo purposes, we'll just set a fake user
        const user = {
          id: 1,
          username: credentials.username,
          email: 'user@example.com'
        }
        
        this.setUser(user)
        localStorage.setItem('access_token', 'fake-jwt-token')
        
        return { success: true, user }
      } catch (error) {
        return { success: false, error: 'Login failed' }
      }
    },
    
    async register(userData) {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        return { success: true }
      } catch (error) {
        return { success: false, error: 'Registration failed' }
      }
    }
  }
})