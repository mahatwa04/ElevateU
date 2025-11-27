import axios from 'axios'

// Get API base URL - for local dev, fallback to production backend
const getAPIBase = (): string => {
  if (typeof window === 'undefined') return 'https://elevateu-backend-777j.onrender.com'
  const hostname = window.location.hostname
  // Use production backend for all (simplest solution for now)
  return 'https://elevateu-backend-777j.onrender.com'
}

// Helper functions
const getAccessToken = () => typeof window !== 'undefined' ? localStorage.getItem('access') : null
const getRefreshToken = () => typeof window !== 'undefined' ? localStorage.getItem('refresh') : null
const setTokens = (access: string, refresh?: string) => {
  localStorage.setItem('access', access)
  if (refresh) localStorage.setItem('refresh', refresh)
}

// Create axios instance
const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false,  // Don't send cookies
})

// Token refresh queue
let isRefreshing = false
let failedQueue: Array<any> = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// Request interceptor - add token and set API base
api.interceptors.request.use((config) => {
  config.baseURL = getAPIBase()
  const token = getAccessToken()
  if (token && config.headers) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle 401 errors with token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = getRefreshToken()
      if (!refreshToken) {
        isRefreshing = false
        return Promise.reject(error)
      }

      try {
        const resp = await axios.post(`${getAPIBase()}/api/auth/token/refresh/`, { refresh: refreshToken })
        const newToken = resp.data.access
        setTokens(newToken, resp.data.refresh)
        api.defaults.headers.common['Authorization'] = 'Bearer ' + newToken
        processQueue(null, newToken)
        return api(originalRequest)
      } catch (err) {
        processQueue(err, null)
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

export { api, setTokens }

