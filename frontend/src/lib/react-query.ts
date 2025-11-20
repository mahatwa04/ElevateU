import React from 'react'
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient()

export const ReactQueryProvider = ({ children }: { children: React.ReactNode }) => {
  return children
}
