// Users API client
import apiClient from './index'

export const usersApi = {
  // Get current user
  getCurrentUser() {
    return apiClient.get('/users/me/')
  },

  // Update user profile
  updateUserProfile(data) {
    return apiClient.put('/users/me/', data)
  }
}