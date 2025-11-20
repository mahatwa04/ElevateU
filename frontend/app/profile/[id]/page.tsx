import React from 'react'
import ProfileHeader from '../../../src/components/ProfileHeader'

interface Props {
  params: { id: string }
}

export default function ProfilePage({ params }: Props) {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-8">
        <ProfileHeader userId={params.id} />
        <section className="mt-6">Profile content goes here</section>
      </div>
    </main>
  )
}
