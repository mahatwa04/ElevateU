import './globals.css'
import React from 'react'
import { Providers } from '../src/providers/Providers'
import { AuthProvider } from '../src/context/AuthContext'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AuthProvider>{children}</AuthProvider>
        </Providers>
      </body>
    </html>
  )
}
