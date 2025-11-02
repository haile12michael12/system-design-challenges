// Project store module
import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    currentProject: null
  }),
  
  getters: {
    getAllProjects: (state) => state.projects,
    getProjectById: (state) => (id) => state.projects.find(p => p.id === id),
    getCurrentProject: (state) => state.currentProject
  },
  
  actions: {
    setProjects(projects) {
      this.projects = projects
    },
    
    setCurrentProject(project) {
      this.currentProject = project
    },
    
    addProject(project) {
      this.projects.push(project)
    },
    
    updateProject(updatedProject) {
      const index = this.projects.findIndex(p => p.id === updatedProject.id)
      if (index !== -1) {
        this.projects.splice(index, 1, updatedProject)
      }
    },
    
    removeProject(id) {
      this.projects = this.projects.filter(p => p.id !== id)
    },
    
    async fetchProjects() {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // For demo purposes, we'll just set some fake projects
        const projects = [
          {
            id: 1,
            name: 'E-commerce Platform',
            description: 'Full-featured online shopping platform',
            created_at: '2025-10-15T09:00:00Z',
            updated_at: '2025-10-20T14:30:00Z'
          },
          {
            id: 2,
            name: 'Mobile Banking App',
            description: 'Secure mobile banking application',
            created_at: '2025-11-01T10:00:00Z',
            updated_at: '2025-11-01T10:00:00Z'
          }
        ]
        
        this.setProjects(projects)
        return { success: true, projects }
      } catch (error) {
        return { success: false, error: 'Failed to fetch projects' }
      }
    }
  }
})