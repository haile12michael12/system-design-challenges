<template>
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
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RequirementCard',
  props: {
    requirement: {
      type: Object,
      required: true
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
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>