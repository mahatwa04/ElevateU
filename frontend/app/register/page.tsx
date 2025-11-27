import React from 'react'
import RegisterForm from '../../src/components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-50">
      {/* Header */}
      <div className="bg-white border-b border-green-100 py-6 px-4">
        <div className="max-w-md mx-auto">
          <h1 className="text-3xl font-bold text-green-600">ElevateU</h1>
          <p className="text-sm text-gray-600 mt-1">Celebrate your achievements</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex items-center justify-center min-h-[calc(100vh-80px)] px-4">
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Account</h2>
          <RegisterForm />
        </div>
      </div>
    </div>
  )
}
