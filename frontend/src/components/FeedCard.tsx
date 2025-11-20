import React from 'react'
import LikeButton from './LikeButton'
import CommentButton from './CommentButton'

interface Props {
  title: string
  body: string
}

export default function FeedCard({ title, body }: Props) {
  return (
    <article className="bg-white rounded shadow p-4 mb-4">
      <h3 className="font-semibold text-lg">{title}</h3>
      <p className="text-sm text-gray-700 mt-2">{body}</p>
      <div className="mt-3 flex gap-2">
        <LikeButton />
        <CommentButton />
      </div>
    </article>
  )
}
