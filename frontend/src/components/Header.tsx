"use client"
import React from 'react'
import Link from 'next/link'
import { useAuthContext } from '../context/AuthContext'
import { useRouter } from 'next/navigation'

export default function Header() {
  const { user, logout } = useAuthContext()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">E</span>
          </div>
          <span className="text-xl font-bold text-gray-900">ElevateU</span>
        </Link>

        <nav className="flex items-center gap-6">
          {user && (
            <>
              <Link href="/" className="text-gray-600 hover:text-gray-900 font-medium">
                Feed
              </Link>
              <Link href="/achievements" className="text-gray-600 hover:text-gray-900 font-medium">
                Achievements
              </Link>
              <Link href="/leaderboard" className="text-gray-600 hover:text-gray-900 font-medium">
                Leaderboard
              </Link>
              <div className="flex items-center gap-4 pl-6 border-l border-gray-200">
                <span className="text-sm text-gray-600">{user.email}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-red-50 text-red-600 rounded hover:bg-red-100 font-medium text-sm"
                >
                  Logout
                </button>
              </div>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
