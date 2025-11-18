"use client"
import React from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { registerSchema, type RegisterSchema } from '../../schemas/authSchema'
import { api } from '../../lib/axios'

export default function RegisterForm() {
  const { register, handleSubmit } = useForm<RegisterSchema>({ resolver: zodResolver(registerSchema) })

  const onSubmit = async (data: RegisterSchema) => {
    if (data.password !== data.confirmPassword) {
      alert('Passwords do not match')
      return
    }
    try {
      await api.post('/api/auth/register/', { email: data.email, password: data.password })
      // show success and prompt for OTP
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      <div>
        <label className="block text-sm">Email</label>
        <input className="w-full border p-2 rounded" {...register('email')} />
      </div>
      <div>
        <label className="block text-sm">Password</label>
        <input type="password" className="w-full border p-2 rounded" {...register('password')} />
      </div>
      <div>
        <label className="block text-sm">Confirm Password</label>
        <input type="password" className="w-full border p-2 rounded" {...register('confirmPassword')} />
      </div>
      <button type="submit" className="w-full py-2 bg-green-600 text-white rounded">Register</button>
    </form>
  )
}
