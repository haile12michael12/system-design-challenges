<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-md">
    <ul class="divide-y divide-gray-200">
      <li v-for="version in versions" :key="version.id">
        <div class="px-4 py-4 sm:px-6">
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-indigo-600 truncate">
              Version {{ version.version_number }}
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
                {{ version.title }}
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
</template>

<script>
export default {
  name: 'VersionList',
  props: {
    versions: {
      type: Array,
      default: () => []
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