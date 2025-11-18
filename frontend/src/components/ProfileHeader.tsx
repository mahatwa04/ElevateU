import React from 'react'
import FollowButton from './FollowButton'

export default function ProfileHeader({ userId }: { userId: string }) {
  return (
    <div className="bg-white rounded shadow p-4 flex items-center gap-4">
      <div className="w-16 h-16 rounded-full bg-gray-200" />
      <div className="flex-1">
        <div className="font-semibold">User {userId}</div>
        <div className="text-sm text-gray-600">University Student</div>
      </div>
      <FollowButton />
    </div>
  )
}
