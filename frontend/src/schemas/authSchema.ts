import { z } from 'zod'

export const registerSchema = z.object({
  email: z.string().email().refine((v) => v.endsWith('@bennett.edu.in'), { message: 'Use your bennett.edu.in email' }),
  password: z.string().min(8),
  confirmPassword: z.string().min(8),
})

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export type RegisterSchema = z.infer<typeof registerSchema>
export type LoginSchema = z.infer<typeof loginSchema>
