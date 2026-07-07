import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getHeaders } from './api'

// Mock the auth store
vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn(),
}))

import { useAuthStore } from '@/stores/auth'

describe('getHeaders', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    // Default mock behavior for localStorage
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => null)
  })

  it('should return headers with token from auth store', () => {
    // Arrange
    useAuthStore.mockReturnValue({ token: 'store-token-123' })

    // Act
    const headers = getHeaders()

    // Assert
    expect(headers).toEqual({
      'Content-Type': 'application/json',
      Authorization: 'Bearer store-token-123',
    })
    expect(useAuthStore).toHaveBeenCalled()
    // Should not check localStorage if store token exists
    // (though in the current implementation, it doesn't short circuit if it uses ||, but standard behavior prioritizes LHS)
  })

  it('should return headers with token from localStorage if store token is not available', () => {
    // Arrange
    useAuthStore.mockReturnValue({ token: null })
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
      if (key === 'access_token') return 'local-storage-token-456'
      return null
    })

    // Act
    const headers = getHeaders()

    // Assert
    expect(headers).toEqual({
      'Content-Type': 'application/json',
      Authorization: 'Bearer local-storage-token-456',
    })
    expect(useAuthStore).toHaveBeenCalled()
    expect(Storage.prototype.getItem).toHaveBeenCalledWith('access_token')
  })

  it('should return headers with Bearer null if no token is available anywhere', () => {
    // Arrange
    useAuthStore.mockReturnValue({ token: null })

    // Act
    const headers = getHeaders()

    // Assert
    expect(headers).toEqual({
      'Content-Type': 'application/json',
      Authorization: 'Bearer null',
    })
  })
})
