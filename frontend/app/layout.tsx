import './globals.css'
import React from 'react'
import { Providers } from '../src/providers/Providers'
import { AuthProvider } from '../src/context/AuthContext'
import Header from '../src/components/Header'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AuthProvider>
            <Header />
            {children}
          </AuthProvider>
        </Providers>
      </body>
    </html>
  )
}
