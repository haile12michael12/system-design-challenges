// Requirement store module
import { defineStore } from 'pinia'

export const useRequirementStore = defineStore('requirement', {
  state: () => ({
    requirements: [],
    currentRequirement: null,
    versions: []
  }),
  
  getters: {
    getAllRequirements: (state) => state.requirements,
    getRequirementById: (state) => (id) => state.requirements.find(r => r.id === id),
    getCurrentRequirement: (state) => state.currentRequirement,
    getVersions: (state) => state.versions
  },
  
  actions: {
    setRequirements(requirements) {
      this.requirements = requirements
    },
    
    setCurrentRequirement(requirement) {
      this.currentRequirement = requirement
    },
    
    setVersions(versions) {
      this.versions = versions
    },
    
    addRequirement(requirement) {
      this.requirements.push(requirement)
    },
    
    updateRequirement(updatedRequirement) {
      const index = this.requirements.findIndex(r => r.id === updatedRequirement.id)
      if (index !== -1) {
        this.requirements.splice(index, 1, updatedRequirement)
      }
    },
    
    removeRequirement(id) {
      this.requirements = this.requirements.filter(r => r.id !== id)
    },
    
    async fetchRequirements() {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // For demo purposes, we'll just set some fake requirements
        const requirements = [
          {
            id: 1,
            title: 'User authentication system',
            description: 'Implement secure user login and registration',
            priority: 'high',
            status: 'in_progress',
            created_at: '2025-11-01T10:00:00Z'
          },
          {
            id: 2,
            title: 'API documentation',
            description: 'Create comprehensive API documentation',
            priority: 'medium',
            status: 'draft',
            created_at: '2025-11-01T11:00:00Z'
          }
        ]
        
        this.setRequirements(requirements)
        return { success: true, requirements }
      } catch (error) {
        return { success: false, error: 'Failed to fetch requirements' }
      }
    },
    
    async fetchRequirement(id) {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // For demo purposes, we'll just return a fake requirement
        const requirement = {
          id: parseInt(id),
          title: 'User authentication system',
          description: 'Implement secure user login and registration with OAuth support',
          priority: 'high',
          status: 'in_progress',
          created_at: '2025-11-01T10:00:00Z',
          updated_at: '2025-11-02T14:30:00Z'
        }
        
        this.setCurrentRequirement(requirement)
        return { success: true, requirement }
      } catch (error) {
        return { success: false, error: 'Failed to fetch requirement' }
      }
    }
  }
})