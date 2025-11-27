"use client"
import React, { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { api } from '../../lib/axios'
import { useAuthContext } from '../../context/AuthContext'

export default function VerifyEmailForm() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const { login } = useAuthContext()
  const email = searchParams.get('email') || ''
  const [otp, setOtp] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const response = await api.post('/api/auth/verify-email/', {
        email,
        otp_code: otp,
      })

      setSuccess(true)
      // Automatically redirect to login after successful verification
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.response?.data?.non_field_errors?.[0] || err?.response?.data || 'Verification failed'
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return <div className="text-green-600 text-center">Email verified! Redirecting to login...</div>
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-sm text-red-600 bg-red-50 p-3 rounded border border-red-200">{error}</div>}
      {success && <div className="text-sm text-green-600 bg-green-50 p-3 rounded border border-green-200">Email verified! Redirecting...</div>}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          value={email}
          disabled
          className="w-full border border-gray-300 p-3 rounded-lg bg-gray-50 text-gray-600"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">6-Digit OTP</label>
        <input
          type="text"
          maxLength={6}
          value={otp}
          onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
          placeholder="000000"
          className="w-full border border-gray-300 p-3 rounded-lg text-center text-2xl tracking-widest font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <button
        type="submit"
        disabled={loading || otp.length !== 6}
        className={`w-full py-3 rounded-lg font-medium transition-all duration-200 ${
          loading || otp.length !== 6 
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
            : 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white hover:shadow-lg hover:shadow-indigo-500/50'
        }`}
      >
        {loading ? 'Verifying...' : 'Verify Email'}
      </button>
    </form>
  )
}
