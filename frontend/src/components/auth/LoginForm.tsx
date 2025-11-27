"use client"
import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema, type LoginSchema } from '../../schemas/authSchema'
import { useAuthContext } from '../../context/AuthContext'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginForm() {
  const { register, handleSubmit, formState } = useForm<LoginSchema>({ resolver: zodResolver(loginSchema) })
  const { login } = useAuthContext()
  const router = useRouter()
  const [apiError, setApiError] = useState<string | null>(null)
  const [testResult, setTestResult] = useState<string | null>(null)

  // Test backend connection
  const testBackend = async () => {
    try {
      const resp = await fetch('https://elevateu-backend-777j.onrender.com/api/health/')
      setTestResult(`✓ Backend OK (${resp.status})`)
    } catch (err: any) {
      setTestResult(`✗ Backend error: ${err.message}`)
    }
  }

  const onSubmit = async (data: LoginSchema) => {
    setApiError(null)
    try {
      console.log('Attempting login with:', { email: data.email })
      console.log('API base URL will be:', process.env.NEXT_PUBLIC_API_BASE)
      await login(data.email, data.password)
      router.push('/')
    } catch (err: any) {
      console.error('Login error details:', {
        message: err?.message,
        code: err?.code,
        responseStatus: err?.response?.status,
        responseData: err?.response?.data,
        fullError: err
      })
      // Try to extract API error message
      let msg = 'Network error'
      if (err?.code === 'ERR_NETWORK') {
        msg = 'Network error - unable to connect to server'
      } else if (err?.code === 'ERR_CORS') {
        msg = 'CORS error - server rejected request'
      } else if (err?.response?.status === 0) {
        msg = 'Connection failed - please check your internet'
      } else if (err?.response?.data?.detail) {
        msg = err.response.data.detail
      } else if (err?.response?.data?.non_field_errors?.[0]) {
        msg = err.response.data.non_field_errors[0]
      } else if (err?.response?.data) {
        msg = typeof err.response.data === 'string' ? err.response.data : JSON.stringify(err.response.data)
      } else if (err?.message) {
        msg = err.message
      }
      setApiError(msg)
    }
  }

  return (
    <div className="space-y-4">
      {testResult && <div className="text-sm bg-blue-50 border border-blue-200 p-2 rounded">{testResult}</div>}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
        {apiError && <div className="text-sm text-red-600 bg-red-50 border border-red-200 p-2 rounded">{apiError}</div>}
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
      <button
        type="button"
        onClick={testBackend}
        className="w-full py-2 rounded bg-gray-200 text-gray-800 text-sm hover:bg-gray-300">
        Test Backend
      </button>
      <p className="text-sm text-center text-gray-600">
        Don't have an account?{' '}
        <Link href="/register" className="text-indigo-600 hover:underline">
          Register here
        </Link>
      </p>
    </div>
  )
}
