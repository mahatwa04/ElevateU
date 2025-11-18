import React from 'react'
import RegisterForm from '../../src/components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-6 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Register</h2>
        <RegisterForm />
      </div>
    </div>
  )
}
