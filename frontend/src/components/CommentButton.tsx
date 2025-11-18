import React from 'react'

export default function CommentButton({ onClick }: { onClick?: () => void }) {
  return (
    <button onClick={onClick} className="px-3 py-1 bg-blue-100 text-blue-700 rounded">Comment</button>
  )
}
