import React from 'react'

const sample = [
  { id: 1, name: 'Alice', points: 120 },
  { id: 2, name: 'Bob', points: 95 },
]

export default function LeaderboardTable() {
  return (
    <div className="bg-white rounded shadow">
      <table className="min-w-full">
        <thead>
          <tr className="text-left">
            <th className="p-3">Rank</th>
            <th className="p-3">User</th>
            <th className="p-3">Points</th>
          </tr>
        </thead>
        <tbody>
          {sample.map((r, i) => (
            <tr key={r.id} className="border-t">
              <td className="p-3">{i + 1}</td>
              <td className="p-3">{r.name}</td>
              <td className="p-3">{r.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
