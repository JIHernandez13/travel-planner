import { afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock localStorage
const localStorageMock: Storage = {
  length: 0,
  clear: vi.fn(),
  getItem: vi.fn(),
  key: vi.fn(),
  removeItem: vi.fn(),
  setItem: vi.fn(),
}

globalThis.localStorage = localStorageMock

// Mock window.location
Object.defineProperty(window, 'location', {
  writable: true,
  value: {
    href: 'http://localhost:3000/',
    origin: 'http://localhost:3000',
    protocol: 'http:',
    host: 'localhost:3000',
    hostname: 'localhost',
    port: '3000',
    pathname: '/',
    search: '',
    hash: '',
  },
})
