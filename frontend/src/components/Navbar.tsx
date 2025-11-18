"use client"
import React from 'react'

export default function Navbar() {
  return (
    <header className="w-full bg-white border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="text-lg font-bold">ElevateU</div>
        <nav className="space-x-4">
          <a href="/" className="text-sm text-gray-700">Feed</a>
          <a href="/achievements" className="text-sm text-gray-700">Achievements</a>
          <a href="/leaderboard" className="text-sm text-gray-700">Leaderboard</a>
        </nav>
      </div>
    </header>
  )
}
