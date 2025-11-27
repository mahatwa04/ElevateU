"use client"
import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { registerSchema, type RegisterSchema } from '../../schemas/authSchema'
import { api } from '../../lib/axios'
import { useRouter } from 'next/navigation'

export default function RegisterForm() {
  const { register, handleSubmit, formState } = useForm<RegisterSchema>({ resolver: zodResolver(registerSchema) })
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const router = useRouter()

  const onSubmit = async (data: RegisterSchema) => {
    setError(null)
    if (data.password !== data.confirmPassword) {
      setError('Passwords do not match')
      return
    }
    
    try {
      // Generate username from email (e.g., S25CSE123 from S25CSE123@bennett.edu.in)
      const username = data.email.split('@')[0]
      
      const response = await api.post('/api/auth/register/', {
        username,
        email: data.email,
        password: data.password,
        password2: data.confirmPassword,
        field_of_interest: 'General',
      })
      
      setSuccess(true)
      // Redirect to OTP verification after 2 seconds
      setTimeout(() => {
        router.push(`/verify-email?email=${encodeURIComponent(data.email)}`)
      }, 1500)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.response?.data?.email?.[0] || err?.response?.data || 'Registration failed'
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    }
  }

  if (success) {
    return <div className="text-green-600 text-center">Registration successful! Redirecting to email verification...</div>
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      {error && <div className="text-sm text-red-600">{error}</div>}
      <div>
        <label className="block text-sm">Email (@bennett.edu.in)</label>
        <input className="w-full border p-2 rounded" {...register('email')} placeholder="S25CSE123@bennett.edu.in" />
      </div>
      <div>
        <label className="block text-sm">Password</label>
        <input type="password" className="w-full border p-2 rounded" {...register('password')} />
      </div>
      <div>
        <label className="block text-sm">Confirm Password</label>
        <input type="password" className="w-full border p-2 rounded" {...register('confirmPassword')} />
      </div>
      <button
        type="submit"
        disabled={formState.isSubmitting}
        className={`w-full py-2 rounded ${formState.isSubmitting ? 'bg-green-300' : 'bg-green-600 text-white'}`}>
        {formState.isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  )
}
