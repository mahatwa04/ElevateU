"use client"
import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema, type LoginSchema } from '../../schemas/authSchema'
import { useAuthContext } from '../../context/AuthContext'
import { useRouter } from 'next/navigation'

export default function LoginForm() {
  const { register, handleSubmit, formState } = useForm<LoginSchema>({ resolver: zodResolver(loginSchema) })
  const { login } = useAuthContext()
  const router = useRouter()
  const [apiError, setApiError] = useState<string | null>(null)

  const onSubmit = async (data: LoginSchema) => {
    setApiError(null)
    try {
      await login(data.email, data.password)
      router.push('/')
    } catch (err: any) {
      // Try to extract API error message
      const msg = err?.response?.data?.detail || err?.response?.data || err?.message || 'Login failed'
      setApiError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      {apiError && <div className="text-sm text-red-600">{apiError}</div>}
      <div>
        <label className="block text-sm">Email</label>
        <input className="w-full border p-2 rounded" {...register('email')} />
      </div>
      <div>
        <label className="block text-sm">Password</label>
        <input type="password" className="w-full border p-2 rounded" {...register('password')} />
      </div>
      <button
        type="submit"
        disabled={formState.isSubmitting}
        className={`w-full py-2 rounded ${formState.isSubmitting ? 'bg-indigo-300' : 'bg-indigo-600 text-white'}`}>
        {formState.isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
