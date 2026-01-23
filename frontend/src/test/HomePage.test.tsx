import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import HomePage from '../HomePage'

// Mock fetch
global.fetch = vi.fn()

describe('HomePage Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render the page title', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    expect(screen.getByRole('heading', { name: /Travel Planner/i, level: 1 })).toBeInTheDocument()
  })

  it('should render the tagline', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    expect(screen.getByText(/Plan your perfect trip/i)).toBeInTheDocument()
  })

  it('should show checking status initially', () => {
    ;(global.fetch as any).mockImplementation(() => new Promise(() => {}))

    render(<HomePage />)
    expect(screen.getByText(/Checking.../i)).toBeInTheDocument()
  })

  it('should show connected status when API is reachable', async () => {
    const mockMessage = 'Welcome to Travel Planner API'
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: mockMessage }),
    })

    render(<HomePage />)

    await waitFor(() => {
      expect(screen.getByText(/✅ Connected/i)).toBeInTheDocument()
    })
  })

  it('should show error status when API is not reachable', async () => {
    ;(global.fetch as any).mockRejectedValue(new Error('Network error'))

    render(<HomePage />)

    await waitFor(() => {
      expect(screen.getByText(/❌ API not reachable/i)).toBeInTheDocument()
    })
  })

  it('should render all feature cards', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)

    expect(screen.getByText(/Plan Trips/i)).toBeInTheDocument()
    expect(screen.getByText(/Track Budget/i)).toBeInTheDocument()
    expect(screen.getByText(/Explore Places/i)).toBeInTheDocument()
  })

  it('should render feature descriptions', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)

    expect(screen.getByText(/Organize your itineraries day by day/i)).toBeInTheDocument()
    expect(screen.getByText(/Keep your spending in check/i)).toBeInTheDocument()
    expect(screen.getByText(/Discover activities and attractions/i)).toBeInTheDocument()
  })

  it('should render Get Started button', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    const button = screen.getByRole('button', { name: /Get Started/i })
    expect(button).toBeInTheDocument()
  })

  it('should render welcome message', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    expect(screen.getByText(/Welcome to Your Travel Planner/i)).toBeInTheDocument()
    expect(screen.getByText(/Start planning your next adventure!/i)).toBeInTheDocument()
  })

  it('should use correct API URL from environment', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })
    global.fetch = mockFetch

    render(<HomePage />)

    await waitFor(() => {
      const expectedUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      expect(mockFetch).toHaveBeenCalledWith(`${expectedUrl}/`)
    })
  })

  it('should have proper class names for styling', () => {
    ;(global.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    const { container } = render(<HomePage />)

    expect(container.querySelector('.home-page')).toBeInTheDocument()
    expect(container.querySelector('.header')).toBeInTheDocument()
    expect(container.querySelector('.content')).toBeInTheDocument()
    expect(container.querySelector('.status-card')).toBeInTheDocument()
    expect(container.querySelector('.welcome-card')).toBeInTheDocument()
    expect(container.querySelector('.features')).toBeInTheDocument()
  })
})
