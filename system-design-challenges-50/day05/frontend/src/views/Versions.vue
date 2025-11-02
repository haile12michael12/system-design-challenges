<template>
  <div class="min-h-full">
    <Navbar />
    <div class="md:pl-64 flex flex-col flex-1">
      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <h1 class="text-2xl font-semibold text-gray-900">Versions</h1>
          </div>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <div class="mt-6">
              <div class="bg-white shadow overflow-hidden sm:rounded-md">
                <ul class="divide-y divide-gray-200">
                  <li v-for="version in versions" :key="version.id">
                    <div class="px-4 py-4 sm:px-6">
                      <div class="flex items-center justify-between">
                        <p class="text-sm font-medium text-indigo-600 truncate">
                          {{ version.title }}
                        </p>
                        <div class="ml-2 flex-shrink-0 flex">
                          <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            {{ version.status }}
                          </p>
                        </div>
                      </div>
                      <div class="mt-2 sm:flex sm:justify-between">
                        <div class="sm:flex">
                          <p class="flex items-center text-sm text-gray-500">
                            Version {{ version.version_number }} • {{ version.description }}
                          </p>
                        </div>
                        <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                          </svg>
                          <p>
                            {{ formatDate(version.created_at) }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'Versions',
  components: {
    Navbar
  },
  data() {
    return {
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
        },
        {
          id: 2,
          requirement_id: 1,
          version_number: 2,
          title: 'User authentication system with OAuth',
          description: 'Added OAuth support for Google and GitHub',
          priority: 'high',
          status: 'in_progress',
          created_at: '2025-11-02T14:30:00Z'
        }
      ]
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>