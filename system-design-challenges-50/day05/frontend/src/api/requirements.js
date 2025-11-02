// Requirements API client
import apiClient from './index'

export const requirementsApi = {
  // Get all requirements
  getAllRequirements(params = {}) {
    return apiClient.get('/requirements/', { params })
  },

  // Get requirement by ID
  getRequirementById(id) {
    return apiClient.get(`/requirements/${id}/`)
  },

  // Create new requirement
  createRequirement(data) {
    return apiClient.post('/requirements/', data)
  },

  // Update requirement
  updateRequirement(id, data) {
    return apiClient.put(`/requirements/${id}/`, data)
  },

  // Delete requirement
  deleteRequirement(id) {
    return apiClient.delete(`/requirements/${id}/`)
  }
}