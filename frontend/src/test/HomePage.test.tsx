import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import HomePage from '../HomePage'

// Mock fetch
globalThis.fetch = vi.fn() as typeof fetch

describe('HomePage Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render the page title', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    expect(screen.getByRole('heading', { name: /Travel Planner/i, level: 1 })).toBeInTheDocument()
  })

  it('should render the tagline', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    expect(screen.getByText(/Plan your perfect trip/i)).toBeInTheDocument()
  })

  it('should show checking status initially', async () => {
    let resolveFetch: (value: Response) => void
    const pendingPromise = new Promise<Response>((resolve) => {
      resolveFetch = resolve
    })
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockReturnValue(pendingPromise)

    render(<HomePage />)
    expect(screen.getByText(/Checking.../i)).toBeInTheDocument()

    // Resolve the pending fetch to avoid leaving an unresolved Promise after the test
    resolveFetch!({
      json: async () => ({ message: 'API running' }),
    })

    await waitFor(() => {
      expect(globalThis.fetch).toHaveBeenCalled()
    })
  })

  it('should show connected status when API is reachable', async () => {
    const mockMessage = 'Welcome to Travel Planner API'
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: mockMessage }),
    })

    render(<HomePage />)

    await waitFor(() => {
      expect(screen.getByText(/✅ Connected/i)).toBeInTheDocument()
    })
  })

  it('should show error status when API is not reachable', async () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockRejectedValue(new Error('Network error'))

    render(<HomePage />)

    await waitFor(() => {
      expect(screen.getByText(/❌ API not reachable/i)).toBeInTheDocument()
    })
  })

  it('should render all feature cards', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)

    expect(screen.getByText(/Plan Trips/i)).toBeInTheDocument()
    expect(screen.getByText(/Track Budget/i)).toBeInTheDocument()
    expect(screen.getByText(/Explore Places/i)).toBeInTheDocument()
  })

  it('should render feature descriptions', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)

    expect(screen.getByText(/Organize your itineraries day by day/i)).toBeInTheDocument()
    expect(screen.getByText(/Keep your spending in check/i)).toBeInTheDocument()
    expect(screen.getByText(/Discover activities and attractions/i)).toBeInTheDocument()
  })

  it('should render Get Started button', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
      json: async () => ({ message: 'API running' }),
    })

    render(<HomePage />)
    const button = screen.getByRole('button', { name: /Get Started/i })
    expect(button).toBeInTheDocument()
  })

  it('should render welcome message', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
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
    globalThis.fetch = mockFetch as typeof fetch

    render(<HomePage />)

    await waitFor(() => {
      const expectedUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      expect(mockFetch).toHaveBeenCalledWith(`${expectedUrl}/`)
    })
  })

  it('should have proper class names for styling', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ;(globalThis.fetch as any).mockResolvedValue({
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
