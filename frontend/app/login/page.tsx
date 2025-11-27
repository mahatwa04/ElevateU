import React from 'react'
import LoginForm from '../../src/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white border-b border-indigo-100 py-6 px-4">
        <div className="max-w-md mx-auto">
          <h1 className="text-3xl font-bold text-indigo-600">ElevateU</h1>
          <p className="text-sm text-gray-600 mt-1">Celebrate your achievements</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex items-center justify-center min-h-[calc(100vh-80px)] px-4">
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Welcome Back</h2>
          <LoginForm />
        </div>
      </div>
    </div>
  )
}
