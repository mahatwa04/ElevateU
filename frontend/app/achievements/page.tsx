import React from 'react'
import AchievementCard from '../../src/components/AchievementCard'

export default function AchievementsPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-8">
        <h1 className="text-2xl font-semibold mb-4">Achievements</h1>
        <AchievementCard title="First Post" description="Awarded for creating first post" />
      </div>
    </main>
  )
}
