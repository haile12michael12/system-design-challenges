// Navigation guards for the application

// Check if user is authenticated
export function isAuthenticated() {
  return !!localStorage.getItem('access_token')
}

// Redirect to login if not authenticated
export function requireAuth(to, from, next) {
  if (!isAuthenticated()) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

// Redirect to dashboard if already authenticated
export function redirectIfAuthenticated(to, from, next) {
  if (isAuthenticated()) {
    next('/dashboard')
  } else {
    next()
  }
}