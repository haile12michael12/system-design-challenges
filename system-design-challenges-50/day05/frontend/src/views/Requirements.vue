<template>
  <div class="min-h-full">
    <Navbar />
    <div class="md:pl-64 flex flex-col flex-1">
      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <div class="flex justify-between items-center">
              <h1 class="text-2xl font-semibold text-gray-900">Requirements</h1>
              <button
                @click="showCreateModal = true"
                class="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create Requirement
              </button>
            </div>
          </div>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <!-- Filters -->
            <div class="mt-6 flex space-x-4">
              <div>
                <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                <select
                  id="status"
                  name="status"
                  class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="">All</option>
                  <option value="draft">Draft</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div>
                <label for="priority" class="block text-sm font-medium text-gray-700">Priority</label>
                <select
                  id="priority"
                  name="priority"
                  class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="">All</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <!-- Requirements List -->
            <div class="mt-6">
              <ul class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <li v-for="requirement in requirements" :key="requirement.id" class="col-span-1 bg-white rounded-lg shadow divide-y divide-gray-200">
                  <div class="w-full flex items-center justify-between p-6 space-x-6">
                    <div class="flex-1 truncate">
                      <div class="flex items-center space-x-3">
                        <h3 class="text-gray-900 text-sm font-medium truncate">{{ requirement.title }}</h3>
                        <span :class="priorityClass(requirement.priority)" class="flex-shrink-0 inline-block px-2 py-0.5 text-xs font-medium rounded-full">
                          {{ requirement.priority }}
                        </span>
                      </div>
                      <p class="mt-1 text-gray-500 text-sm truncate">{{ requirement.description }}</p>
                    </div>
                  </div>
                  <div>
                    <div class="-mt-px flex divide-x divide-gray-200">
                      <div class="w-0 flex-1 flex">
                        <router-link
                          :to="`/requirements/${requirement.id}`"
                          class="relative -mr-px w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-bl-lg hover:text-gray-500"
                        >
                          <svg class="w-5 h-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                          </svg>
                          <span class="ml-3">View</span>
                        </router-link>
                      </div>
                      <div class="-ml-px w-0 flex-1 flex">
                        <button
                          @click="editRequirement(requirement)"
                          class="relative w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-br-lg hover:text-gray-500"
                        >
                          <svg class="w-5 h-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                          </svg>
                          <span class="ml-3">Edit</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  {{ editingRequirement ? 'Edit Requirement' : 'Create Requirement' }}
                </h3>
                <div class="mt-4">
                  <form @submit.prevent="saveRequirement">
                    <div class="mb-4">
                      <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
                      <input
                        type="text"
                        id="title"
                        v-model="form.title"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        required
                      />
                    </div>
                    <div class="mb-4">
                      <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                      <textarea
                        id="description"
                        v-model="form.description"
                        rows="3"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      ></textarea>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <label for="priority" class="block text-sm font-medium text-gray-700">Priority</label>
                        <select
                          id="priority"
                          v-model="form.priority"
                          class="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>
                      <div>
                        <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                        <select
                          id="status"
                          v-model="form.status"
                          class="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        >
                          <option value="draft">Draft</option>
                          <option value="in_progress">In Progress</option>
                          <option value="completed">Completed</option>
                        </select>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="saveRequirement"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Save
            </button>
            <button
              type="button"
              @click="showCreateModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'Requirements',
  components: {
    Navbar
  },
  data() {
    return {
      requirements: [
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
      ],
      showCreateModal: false,
      editingRequirement: null,
      form: {
        title: '',
        description: '',
        priority: 'medium',
        status: 'draft'
      }
    }
  },
  methods: {
    priorityClass(priority) {
      const classes = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-red-100 text-red-800'
      }
      return classes[priority] || classes.medium
    },
    editRequirement(requirement) {
      this.editingRequirement = requirement
      this.form = { ...requirement }
      this.showCreateModal = true
    },
    saveRequirement() {
      if (this.editingRequirement) {
        // Update existing requirement
        const index = this.requirements.findIndex(r => r.id === this.editingRequirement.id)
        if (index !== -1) {
          this.requirements.splice(index, 1, { ...this.editingRequirement, ...this.form })
        }
      } else {
        // Create new requirement
        const newRequirement = {
          id: this.requirements.length + 1,
          ...this.form,
          created_at: new Date().toISOString()
        }
        this.requirements.push(newRequirement)
      }
      
      // Reset form and close modal
      this.resetForm()
      this.showCreateModal = false
    },
    resetForm() {
      this.editingRequirement = null
      this.form = {
        title: '',
        description: '',
        priority: 'medium',
        status: 'draft'
      }
    }
  }
}
</script>