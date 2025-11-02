// Projects API client
import apiClient from './index'

export const projectsApi = {
  // Get all projects
  getAllProjects(params = {}) {
    return apiClient.get('/projects/', { params })
  },

  // Get project by ID
  getProjectById(id) {
    return apiClient.get(`/projects/${id}/`)
  },

  // Create new project
  createProject(data) {
    return apiClient.post('/projects/', data)
  },

  // Update project
  updateProject(id, data) {
    return apiClient.put(`/projects/${id}/`, data)
  },

  // Delete project
  deleteProject(id) {
    return apiClient.delete(`/projects/${id}/`)
  }
}