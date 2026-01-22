import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// TypeScript interfaces for API data types
export interface TripData {
  id?: number
  title: string
  description?: string
  destination: string
  start_date: string
  end_date: string
  budget?: number
  user_id?: number
}

export interface UserRegistration {
  email: string
  username: string
  password: string
}

export interface LoginCredentials {
  username: string
  password: string
}

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Security Note: localStorage is vulnerable to XSS attacks.
// For production, consider using httpOnly cookies or implementing
// Content Security Policy headers to mitigate XSS risks.

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: async (userData: UserRegistration) => {
    const response = await apiClient.post('/api/v1/auth/register', userData)
    return response.data
  },
  
  login: async (credentials: LoginCredentials) => {
    const response = await apiClient.post('/api/v1/auth/login', credentials)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  },
  
  logout: () => {
    localStorage.removeItem('access_token')
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  },
}

// Trips API (placeholder for future implementation)
export const tripsAPI = {
  getAll: async () => {
    const response = await apiClient.get('/api/v1/trips')
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await apiClient.get(`/api/v1/trips/${id}`)
    return response.data
  },
  
  create: async (tripData: TripData) => {
    const response = await apiClient.post('/api/v1/trips', tripData)
    return response.data
  },
  
  update: async (id: number, tripData: Partial<TripData>) => {
    const response = await apiClient.put(`/api/v1/trips/${id}`, tripData)
    return response.data
  },
  
  delete: async (id: number) => {
    const response = await apiClient.delete(`/api/v1/trips/${id}`)
    return response.data
  },
}

export default apiClient
