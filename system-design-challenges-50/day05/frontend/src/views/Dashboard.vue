<template>
  <div class="min-h-full">
    <Navbar />
    <div class="md:pl-64 flex flex-col flex-1">
      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
          </div>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <!-- Stats -->
            <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                      <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <div class="ml-5 w-0 flex-1">
                      <dl>
                        <dt class="text-sm font-medium text-gray-500 truncate">Total Requirements</dt>
                        <dd class="flex items-baseline">
                          <div class="text-2xl font-semibold text-gray-900">12</div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-green-500 rounded-md p-3">
                      <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div class="ml-5 w-0 flex-1">
                      <dl>
                        <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                        <dd class="flex items-baseline">
                          <div class="text-2xl font-semibold text-gray-900">8</div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                      <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div class="ml-5 w-0 flex-1">
                      <dl>
                        <dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
                        <dd class="flex items-baseline">
                          <div class="text-2xl font-semibold text-gray-900">4</div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Requirements -->
            <div class="mt-8">
              <h2 class="text-lg font-medium text-gray-900">Recent Requirements</h2>
              <div class="mt-4">
                <div class="bg-white shadow overflow-hidden sm:rounded-md">
                  <ul class="divide-y divide-gray-200">
                    <li>
                      <a href="#" class="block hover:bg-gray-50">
                        <div class="px-4 py-4 sm:px-6">
                          <div class="flex items-center justify-between">
                            <p class="text-sm font-medium text-indigo-600 truncate">User authentication system</p>
                            <div class="ml-2 flex-shrink-0 flex">
                              <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                Completed
                              </p>
                            </div>
                          </div>
                          <div class="mt-2 sm:flex sm:justify-between">
                            <div class="sm:flex">
                              <p class="flex items-center text-sm text-gray-500">
                                High priority requirement
                              </p>
                            </div>
                            <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                              <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                              </svg>
                              <p>
                                Created on Nov 1, 2025
                              </p>
                            </div>
                          </div>
                        </div>
                      </a>
                    </li>
                  </ul>
                </div>
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
  name: 'Dashboard',
  components: {
    Navbar
  }
}
</script>