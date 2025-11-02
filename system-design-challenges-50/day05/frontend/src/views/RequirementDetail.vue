<template>
  <div class="min-h-full">
    <Navbar />
    <div class="md:pl-64 flex flex-col flex-1">
      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <div class="flex justify-between items-center">
              <h1 class="text-2xl font-semibold text-gray-900">Requirement Details</h1>
              <button
                @click="editMode = true"
                v-if="!editMode"
                class="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Edit
              </button>
            </div>
          </div>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <div v-if="!editMode" class="mt-6">
              <div class="bg-white shadow overflow-hidden sm:rounded-lg">
                <div class="px-4 py-5 sm:px-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">
                    {{ requirement.title }}
                  </h3>
                  <p class="mt-1 max-w-2xl text-sm text-gray-500">
                    {{ requirement.description }}
                  </p>
                </div>
                <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
                  <dl class="sm:divide-y sm:divide-gray-200">
                    <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                      <dt class="text-sm font-medium text-gray-500">
                        Priority
                      </dt>
                      <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        <span :class="priorityClass">{{ requirement.priority }}</span>
                      </dd>
                    </div>
                    <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                      <dt class="text-sm font-medium text-gray-500">
                        Status
                      </dt>
                      <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        {{ requirement.status }}
                      </dd>
                    </div>
                    <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                      <dt class="text-sm font-medium text-gray-500">
                        Created
                      </dt>
                      <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        {{ formatDate(requirement.created_at) }}
                      </dd>
                    </div>
                    <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                      <dt class="text-sm font-medium text-gray-500">
                        Last Updated
                      </dt>
                      <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                        {{ formatDate(requirement.updated_at) }}
                      </dd>
                    </div>
                  </dl>
                </div>
              </div>

              <!-- Versions Section -->
              <div class="mt-8">
                <div class="flex justify-between items-center">
                  <h2 class="text-lg font-medium text-gray-900">Versions</h2>
                  <button
                    @click="showVersionModal = true"
                    class="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Create Version
                  </button>
                </div>
                <div class="mt-4">
                  <VersionList :versions="versions" />
                </div>
              </div>
            </div>

            <!-- Edit Form -->
            <div v-else class="mt-6">
              <div class="bg-white shadow sm:rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Edit Requirement</h3>
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
                        <Editor v-model="form.description" />
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
                      <div class="mt-6 flex justify-end">
                        <button
                          type="button"
                          @click="editMode = false"
                          class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Cancel
                        </button>
                        <button
                          type="submit"
                          class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Save
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Create Version Modal -->
    <div v-if="showVersionModal" class="fixed z-10 inset-0 overflow-y-auto">
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
                  Create New Version
                </h3>
                <div class="mt-4">
                  <form @submit.prevent="createVersion">
                    <div class="mb-4">
                      <label for="version-title" class="block text-sm font-medium text-gray-700">Title</label>
                      <input
                        type="text"
                        id="version-title"
                        v-model="versionForm.title"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        required
                      />
                    </div>
                    <div class="mb-4">
                      <label for="version-description" class="block text-sm font-medium text-gray-700">Description</label>
                      <textarea
                        id="version-description"
                        v-model="versionForm.description"
                        rows="3"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      ></textarea>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <label for="version-priority" class="block text-sm font-medium text-gray-700">Priority</label>
                        <select
                          id="version-priority"
                          v-model="versionForm.priority"
                          class="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>
                      <div>
                        <label for="version-status" class="block text-sm font-medium text-gray-700">Status</label>
                        <select
                          id="version-status"
                          v-model="versionForm.status"
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
              @click="createVersion"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Create
            </button>
            <button
              type="button"
              @click="showVersionModal = false"
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
import VersionList from '@/components/VersionList.vue'
import Editor from '@/components/Editor.vue'

export default {
  name: 'RequirementDetail',
  components: {
    Navbar,
    VersionList,
    Editor
  },
  data() {
    return {
      requirement: {
        id: 1,
        title: 'User authentication system',
        description: 'Implement secure user login and registration with OAuth support',
        priority: 'high',
        status: 'in_progress',
        created_at: '2025-11-01T10:00:00Z',
        updated_at: '2025-11-02T14:30:00Z'
      },
      versions: [
        {
          id: 1,
          requirement_id: 1,
          version_number: 1,
          title: 'User authentication system',
          description: 'Initial version of the authentication system',
          priority: 'high',
          status: 'completed',
          created_at: '2025-11-01T10:00:00Z'
        }
      ],
      editMode: false,
      showVersionModal: false,
      form: {
        title: '',
        description: '',
        priority: 'medium',
        status: 'draft'
      },
      versionForm: {
        title: '',
        description: '',
        priority: 'medium',
        status: 'draft'
      }
    }
  },
  computed: {
    priorityClass() {
      const classes = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-red-100 text-red-800'
      }
      return `px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${classes[this.requirement.priority] || classes.medium}`
    }
  },
  created() {
    // Initialize form with requirement data
    this.form = { ...this.requirement }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString()
    },
    saveRequirement() {
      // Update requirement with form data
      this.requirement = { ...this.requirement, ...this.form, updated_at: new Date().toISOString() }
      this.editMode = false
    },
    createVersion() {
      // Create new version
      const newVersion = {
        id: this.versions.length + 1,
        requirement_id: this.requirement.id,
        version_number: this.versions.length + 1,
        ...this.versionForm,
        created_at: new Date().toISOString()
      }
      this.versions.push(newVersion)
      
      // Reset form and close modal
      this.versionForm = {
        title: '',
        description: '',
        priority: 'medium',
        status: 'draft'
      }
      this.showVersionModal = false
    }
  }
}
</script>