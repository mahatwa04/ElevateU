import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Simple token helpers. For production, prefer httpOnly cookies.
const getAccessToken = () => typeof window !== 'undefined' ? localStorage.getItem('access') : null
const getRefreshToken = () => typeof window !== 'undefined' ? localStorage.getItem('refresh') : null
const setTokens = (access: string, refresh?: string) => {
  localStorage.setItem('access', access)
  if (refresh) localStorage.setItem('refresh', refresh)
}

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

api.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token && config.headers) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

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
        const resp = await axios.post(`${API_BASE}/api/auth/token/refresh/`, { refresh: refreshToken })
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
