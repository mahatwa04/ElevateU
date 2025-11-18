"use client"
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { api, setTokens } from '../lib/axios'

type User = {
  id: number
  email: string
  username?: string
  campus_verified?: boolean
  [key: string]: any
}

type AuthContextValue = {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshTokens: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

const ACCESS_KEY = 'access'
const REFRESH_KEY = 'refresh'

const readToken = (key: string) => (typeof window !== 'undefined' ? localStorage.getItem(key) : null)
const removeToken = (key: string) => typeof window !== 'undefined' && localStorage.removeItem(key)

async function fetchMe() {
  const resp = await api.get('/api/auth/me/')
  return resp.data
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const queryClient = useQueryClient()
  const [accessToken, setAccessToken] = useState<string | null>(() => readToken(ACCESS_KEY))
  const [refreshToken, setRefreshTokenState] = useState<string | null>(() => readToken(REFRESH_KEY))

  // React Query to fetch user profile when access token exists
  const { data: user, refetch, isLoading } = useQuery(['auth', 'me'], fetchMe, {
    enabled: !!accessToken,
    retry: false,
    onError: () => {
      // if fetchMe fails, clear tokens
    },
  })

  useEffect(() => {
    const a = readToken(ACCESS_KEY)
    const r = readToken(REFRESH_KEY)
    setAccessToken(a)
    setRefreshTokenState(r)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const resp = await api.post('/api/auth/token/', { email, password })
    const access = resp.data.access
    const refresh = resp.data.refresh
    setTokens(access, refresh)
    setAccessToken(access)
    setRefreshTokenState(refresh)
    await queryClient.invalidateQueries(['auth', 'me'])
    await refetch()
  }, [queryClient, refetch])

  const logout = useCallback(() => {
    removeToken(ACCESS_KEY)
    removeToken(REFRESH_KEY)
    setAccessToken(null)
    setRefreshTokenState(null)
    queryClient.setQueryData(['auth', 'me'], null)
  }, [queryClient])

  const refreshTokens = useCallback(async () => {
    const refresh = readToken(REFRESH_KEY)
    if (!refresh) throw new Error('No refresh token available')
    const resp = await api.post('/api/auth/token/refresh/', { refresh })
    const access = resp.data.access
    const newRefresh = resp.data.refresh
    setTokens(access, newRefresh)
    setAccessToken(access)
    setRefreshTokenState(newRefresh)
    await queryClient.invalidateQueries(['auth', 'me'])
  }, [queryClient])

  const value: AuthContextValue = {
    user: (user as User) || null,
    accessToken,
    refreshToken,
    loading: isLoading,
    login,
    logout,
    refreshTokens,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuthContext must be used within AuthProvider')
  return ctx
}
