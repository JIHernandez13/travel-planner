import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock axios before importing api module
vi.mock('axios', () => {
  const mockAxiosInstance = {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn(), eject: vi.fn() },
      response: { use: vi.fn(), eject: vi.fn() },
    },
  }

  return {
    default: {
      create: vi.fn(() => mockAxiosInstance),
      mockAxiosInstance, // Export for testing
    },
  }
})

import axios from 'axios'
import { authAPI, tripsAPI } from '../api'

// Get the mock instance
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const mockAxiosInstance = (axios as any).mockAxiosInstance || {
  post: vi.fn(),
  get: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
}

describe('API Module', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    if (localStorage.clear) {
      localStorage.clear()
    }
  })

  describe('authAPI', () => {
    describe('register', () => {
      it('should register a new user', async () => {
        const userData = {
          email: 'test@example.com',
          username: 'testuser',
          password: 'password123',
        }

        const mockResponse = {
          data: {
            id: 1,
            email: userData.email,
            username: userData.username,
          },
        }

        mockAxiosInstance.post.mockResolvedValue(mockResponse)

        const result = await authAPI.register(userData)
        expect(result).toEqual(mockResponse.data)
        expect(mockAxiosInstance.post).toHaveBeenCalled()
      })
    })

    describe('login', () => {
      it('should login user and store access token', async () => {
        const credentials = {
          username: 'testuser',
          password: 'password123',
        }

        const mockResponse = {
          data: {
            access_token: 'test-token-123',
            token_type: 'bearer',
          },
        }

        mockAxiosInstance.post.mockResolvedValue(mockResponse)

        const result = await authAPI.login(credentials)

        expect(mockAxiosInstance.post).toHaveBeenCalled()
        expect(result).toEqual(mockResponse.data)
        expect(localStorage.setItem).toHaveBeenCalledWith('access_token', 'test-token-123')
      })

      it('should not store token if not returned', async () => {
        const credentials = {
          username: 'testuser',
          password: 'password123',
        }

        const mockResponse = {
          data: {},
        }

        mockAxiosInstance.post.mockResolvedValue(mockResponse)

        await authAPI.login(credentials)
        expect(localStorage.setItem).not.toHaveBeenCalled()
      })
    })

    describe('logout', () => {
      it('should remove access token from localStorage', () => {
        localStorage.setItem('access_token', 'test-token')
        authAPI.logout()
        expect(localStorage.removeItem).toHaveBeenCalledWith('access_token')
      })
    })

    describe('getCurrentUser', () => {
      it('should fetch current user data', async () => {
        const mockUser = {
          id: 1,
          email: 'test@example.com',
          username: 'testuser',
        }

        const mockResponse = {
          data: mockUser,
        }

        mockAxiosInstance.get.mockResolvedValue(mockResponse)

        const result = await authAPI.getCurrentUser()
        expect(result).toEqual(mockUser)
        expect(mockAxiosInstance.get).toHaveBeenCalled()
      })
    })
  })

  describe('tripsAPI', () => {
    const mockTrip = {
      id: 1,
      title: 'Test Trip',
      destination: 'Paris',
      start_date: '2024-01-01',
      end_date: '2024-01-10',
    }

    describe('getAll', () => {
      it('should fetch all trips', async () => {
        const mockResponse = {
          data: [mockTrip],
        }

        mockAxiosInstance.get.mockResolvedValue(mockResponse)

        const result = await tripsAPI.getAll()
        expect(result).toEqual([mockTrip])
      })
    })

    describe('getById', () => {
      it('should fetch trip by id', async () => {
        const mockResponse = {
          data: mockTrip,
        }

        mockAxiosInstance.get.mockResolvedValue(mockResponse)

        const result = await tripsAPI.getById(1)
        expect(result).toEqual(mockTrip)
      })
    })

    describe('create', () => {
      it('should create a new trip', async () => {
        const tripData = {
          title: 'New Trip',
          destination: 'Tokyo',
          start_date: '2024-02-01',
          end_date: '2024-02-10',
        }

        const mockResponse = {
          data: { id: 2, ...tripData },
        }

        mockAxiosInstance.post.mockResolvedValue(mockResponse)

        const result = await tripsAPI.create(tripData)
        expect(result).toEqual({ id: 2, ...tripData })
      })
    })

    describe('update', () => {
      it('should update a trip', async () => {
        const tripData = {
          title: 'Updated Trip',
        }

        const mockResponse = {
          data: { ...mockTrip, ...tripData },
        }

        mockAxiosInstance.put.mockResolvedValue(mockResponse)

        const result = await tripsAPI.update(1, tripData)
        expect(result.title).toBe('Updated Trip')
      })
    })

    describe('delete', () => {
      it('should delete a trip', async () => {
        const mockResponse = {
          data: { message: 'Trip deleted' },
        }

        mockAxiosInstance.delete.mockResolvedValue(mockResponse)

        const result = await tripsAPI.delete(1)
        expect(result).toEqual({ message: 'Trip deleted' })
      })
    })
  })

  describe('API Configuration', () => {
    it('should use correct base URL from environment', () => {
      expect(import.meta.env.VITE_API_URL || 'http://localhost:8000').toBeTruthy()
    })
  })
})
