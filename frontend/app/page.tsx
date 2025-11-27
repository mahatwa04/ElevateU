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
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
      <div className="max-w-3xl mx-auto py-8 px-4">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Achievement Feed</h1>
            <p className="text-indigo-300 text-sm">Celebrate and inspire your community</p>
          </div>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg hover:shadow-indigo-500/50 transition-all duration-300"
          >
            + Create Achievement
          </button>
        </div>
        <CreatePostModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
        {posts && posts.length > 0 ? (
          <div className="space-y-6">
            {posts.map((post) => (
              <article key={post.id} className="bg-white/10 backdrop-blur-md rounded-lg shadow-lg p-6 border border-white/20 hover:border-indigo-500/50 hover:shadow-indigo-500/20 transition-all duration-300">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-indigo-200 font-medium text-sm">{post.user}</p>
                    <span className="text-xs text-gray-400">{new Date(post.created_at).toLocaleDateString()}</span>
                  </div>
                  {post.category && (
                    <span className="px-3 py-1 bg-gradient-to-r from-indigo-500/40 to-purple-500/40 text-indigo-100 text-xs rounded-full border border-indigo-400/30">
                      {post.category}
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-xl text-white mb-3">{post.title}</h3>
                <p className="text-gray-200 text-sm leading-relaxed mb-4">{post.description}</p>
                <div className="flex gap-6 text-sm text-gray-300 border-t border-white/10 pt-4">
                  <button className="hover:text-indigo-300 transition-colors">👍 {post.like_count} likes</button>
                  <button className="hover:text-indigo-300 transition-colors">💬 {post.comment_count} comments</button>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">📝</div>
            <p className="text-gray-300 text-lg">No achievements yet</p>
            <p className="text-gray-400 text-sm mt-2">Be the first to share your success!</p>
          </div>
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
