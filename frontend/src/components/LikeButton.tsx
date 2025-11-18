import React from 'react'

export default function LikeButton({ onClick }: { onClick?: () => void }) {
  return (
    <button onClick={onClick} className="px-3 py-1 bg-red-100 text-red-700 rounded">Like</button>
  )
}
