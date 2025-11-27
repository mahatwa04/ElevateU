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
      {error && <div className="text-sm text-red-600">{error}</div>}
      <div>
        <label className="block text-sm">Email</label>
        <input
          type="email"
          value={email}
          disabled
          className="w-full border p-2 rounded bg-gray-100"
        />
      </div>
      <div>
        <label className="block text-sm">6-Digit OTP</label>
        <input
          type="text"
          maxLength={6}
          value={otp}
          onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
          placeholder="000000"
          className="w-full border p-2 rounded text-center text-2xl tracking-widest"
        />
      </div>
      <button
        type="submit"
        disabled={loading || otp.length !== 6}
        className={`w-full py-2 rounded ${
          loading || otp.length !== 6 ? 'bg-blue-300' : 'bg-blue-600 text-white'
        }`}
      >
        {loading ? 'Verifying...' : 'Verify'}
      </button>
    </form>
  )
}
