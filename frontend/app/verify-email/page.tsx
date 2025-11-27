import React, { Suspense } from 'react'
import VerifyEmailForm from '../../src/components/auth/VerifyEmailForm'

export default function VerifyEmailPage() {
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
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Verify Email</h2>
          <p className="text-sm text-gray-600 mb-6">Enter the 6-digit OTP sent to your email</p>
          <Suspense fallback={<div>Loading...</div>}>
            <VerifyEmailForm />
          </Suspense>
        </div>
      </div>
    </div>
  )
}
