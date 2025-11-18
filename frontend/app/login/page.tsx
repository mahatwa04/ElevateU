import React from 'react'
import LoginForm from '../../src/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-6 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Login</h2>
        <LoginForm />
      </div>
    </div>
  )
}
