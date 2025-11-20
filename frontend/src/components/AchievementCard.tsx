import React from 'react'

interface Props {
  title: string
  description?: string
}

export default function AchievementCard({ title, description }: Props) {
  return (
    <div className="bg-white rounded shadow p-4 mb-4">
      <div className="text-sm text-indigo-600 font-semibold">Achievement</div>
      <h3 className="font-semibold text-lg mt-1">{title}</h3>
      {description && <p className="text-sm text-gray-700 mt-2">{description}</p>}
    </div>
  )
}
