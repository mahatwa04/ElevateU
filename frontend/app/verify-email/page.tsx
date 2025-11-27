import React from 'react'
import VerifyEmailForm from '../../src/components/auth/VerifyEmailForm'

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-6 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Verify Email</h2>
        <p className="text-sm text-gray-600 mb-4">Enter the 6-digit OTP sent to your email</p>
        <VerifyEmailForm />
      </div>
    </div>
  )
}
