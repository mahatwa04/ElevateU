// api-client.js - Wire static HTML forms to Django backend

function getAPIBase() {
  if (typeof window === 'undefined') return 'http://127.0.0.1:8000'
  const hostname = window.location.hostname
  const port = window.location.port
  
  // If accessing from localhost:3000 (Next.js dev), use 127.0.0.1 backend (Windows fix)
  if ((hostname === 'localhost' || hostname === '127.0.0.1') && (port === '3000' || port === '3001')) {
    return 'http://127.0.0.1:8000'
  }
  
  // If accessing from any localhost/127.0.0.1, try 127.0.0.1:8000
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://127.0.0.1:8000'
  }
  
  // Otherwise use production backend
  return 'https://elevateu-backend-777j.onrender.com'
}

const API_BASE = getAPIBase()
console.log('API Base URL:', API_BASE)

class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL
    this.accessToken = null
    this.refreshToken = null
    this.loadTokens()
  }

  loadTokens() {
    this.accessToken = localStorage.getItem('access')
    this.refreshToken = localStorage.getItem('refresh')
  }

  saveTokens(access, refresh) {
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    this.accessToken = access
    this.refreshToken = refresh
  }

  clearTokens() {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    this.accessToken = null
    this.refreshToken = null
  }

  async request(endpoint, method = 'GET', body = null) {
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }

    const options = {
      method,
      headers,
      mode: 'cors',
    }

    if (body) {
      options.body = JSON.stringify(body)
    }

    try {
      console.log('API Request:', {
        url: `${this.baseURL}${endpoint}`,
        method,
        body: body ? JSON.stringify(body) : null,
        headers
      })

      const response = await fetch(`${this.baseURL}${endpoint}`, options)
      
      console.log('API Response status:', response.status)

      if (!response.ok) {
        let errorData
        try {
          errorData = await response.json()
        } catch {
          errorData = { detail: response.statusText }
        }
        
        console.error('API Error:', errorData)
        
        // If 401 (Unauthorized), clear tokens and redirect to login
        if (response.status === 401) {
          this.clearTokens()
          // Redirect to login page
          if (typeof window !== 'undefined') {
            window.location.href = 'login.html'
          }
          const error = new Error('Session expired. Please login again.')
          error.response = { data: errorData, status: response.status }
          throw error
        }
        
        // Format error message from Django
        let errorMsg = 'Request failed'
        if (errorData.detail) {
          errorMsg = errorData.detail
        } else if (errorData.password) {
          errorMsg = 'Password: ' + (Array.isArray(errorData.password) ? errorData.password[0] : errorData.password)
        } else if (errorData.email) {
          errorMsg = 'Email: ' + (Array.isArray(errorData.email) ? errorData.email[0] : errorData.email)
        } else if (errorData.username) {
          errorMsg = 'Username: ' + (Array.isArray(errorData.username) ? errorData.username[0] : errorData.username)
        } else if (typeof errorData === 'object') {
          errorMsg = Object.entries(errorData)
            .map(([key, val]) => `${key}: ${Array.isArray(val) ? val[0] : val}`)
            .join(', ')
        }
        
        const error = new Error(errorMsg)
        error.response = { data: errorData, status: response.status }
        throw error
      }

      const data = await response.json()
      console.log('API Response data:', data)
      return data
    } catch (error) {
      console.error('API Error caught:', error)
      throw error
    }
  }

  async register(email, password, name) {
    const username = email.split('@')[0]
    const data = await this.request('/api/auth/register/', 'POST', {
      username,
      email,
      password,
      password2: password,
      first_name: name,
      field_of_interest: 'General',
    })
    return data
  }

  async login(email, password) {
    const data = await this.request('/api/auth/token/', 'POST', {
      email,
      password,
    })
    this.saveTokens(data.access, data.refresh)
    return data
  }

  async getMe() {
    return this.request('/api/auth/me/')
  }

  async updateProfile(data) {
    return this.request('/api/auth/me/', 'PATCH', data)
  }

  async getPosts() {
    return this.request('/api/posts/')
  }

  async createPost(title, description, category = 'General') {
    return this.request('/api/posts/', 'POST', {
      title,
      description,
      category,
    })
  }

  async logout() {
    this.clearTokens()
  }
}

const api = new APIClient(API_BASE)
