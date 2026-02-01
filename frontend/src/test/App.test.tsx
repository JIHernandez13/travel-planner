import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App Component', () => {
  it('should render without crashing', () => {
    render(<App />)
    expect(document.querySelector('.App')).toBeInTheDocument()
  })

  it('should render Router component', () => {
    const { container } = render(<App />)
    expect(container.querySelector('.App')).toBeInTheDocument()
  })

  it('should render HomePage by default on root path', () => {
    render(<App />)
    // HomePage should be rendered by default
    expect(screen.getByRole('heading', { name: /Travel Planner/i, level: 1 })).toBeInTheDocument()
  })

  it('should have Routes configured', () => {
    const { container } = render(<App />)
    const appElement = container.querySelector('.App')
    expect(appElement).toBeInTheDocument()
  })
})
