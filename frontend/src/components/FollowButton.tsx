import React from 'react'

export default function FollowButton({ following, onClick }: { following?: boolean; onClick?: () => void }) {
  return (
    <button onClick={onClick} className={`px-3 py-1 rounded ${following ? 'bg-gray-200' : 'bg-green-100 text-green-800'}`}>
      {following ? 'Following' : 'Follow'}
    </button>
  )
}
