"use client"
import React, { useState } from 'react'
import ProtectedRoute from '../src/components/ProtectedRoute'
import { usePosts } from '../src/hooks/usePosts'
import CreatePostModal from '../src/components/posts/CreatePostModal'

function FeedContent() {
  const { data: posts, isLoading, error } = usePosts()
  const [isModalOpen, setIsModalOpen] = useState(false)

  if (isLoading) return <div className="text-center py-8">Loading posts...</div>
  if (error) return <div className="text-center py-8 text-red-600">Error loading posts</div>

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-semibold">Feed</h1>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
          >
            Create Achievement
          </button>
        </div>
        <CreatePostModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
        {posts && posts.length > 0 ? (
          <div className="space-y-4">
            {posts.map((post) => (
              <article key={post.id} className="bg-white rounded shadow p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">{post.user}</span>
                  <span className="text-xs text-gray-400">{new Date(post.created_at).toLocaleDateString()}</span>
                </div>
                <h3 className="font-semibold text-lg">{post.title}</h3>
                <p className="text-sm text-gray-700 mt-2">{post.description}</p>
                {post.category && <span className="inline-block mt-2 px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded">{post.category}</span>}
                <div className="mt-3 flex gap-4 text-sm text-gray-600">
                  <span>👍 {post.like_count} likes</span>
                  <span>💬 {post.comment_count} comments</span>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">No posts yet. Start creating!</div>
        )}
      </div>
    </main>
  )
}

export default function Page() {
  return (
    <ProtectedRoute>
      <FeedContent />
    </ProtectedRoute>
  )
}
