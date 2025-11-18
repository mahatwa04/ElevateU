import React from 'react'
import LeaderboardTable from '../../src/components/LeaderboardTable'

export default function LeaderboardPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8">
        <h1 className="text-2xl font-semibold mb-4">Leaderboard</h1>
        <LeaderboardTable />
      </div>
    </main>
  )
}
