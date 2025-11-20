"use client"
import React, { useState, useRef } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreatePost } from '../../hooks/usePosts'

const createPostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  description: z.string().min(1, 'Description is required'),
  category: z.string().optional(),
  image: z.string().url().optional().or(z.literal('')),
})

type CreatePostSchema = z.infer<typeof createPostSchema>

interface Props {
  isOpen: boolean
  onClose: () => void
}

export default function CreatePostModal({ isOpen, onClose }: Props) {
  const { register, handleSubmit, formState, reset } = useForm<CreatePostSchema>({
    resolver: zodResolver(createPostSchema),
  })
  const { mutate: createPost, isPending, error } = useCreatePost()
  const [apiError, setApiError] = useState<string | null>(null)

  // Close on escape and trap focus inside the dialog for a11y
  React.useEffect(() => {
    if (!isOpen) return

    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }

    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [isOpen, onClose])

  // Focus trap: keep focus inside the modal while open
  const containerRef = useRef<HTMLDivElement | null>(null)
  React.useEffect(() => {
    if (!isOpen) return

    const el = containerRef.current
    if (!el) return

    const focusable = el.querySelectorAll<HTMLElement>(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    )

    const first = focusable[0]
    const last = focusable[focusable.length - 1]

    const handleKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault()
          last?.focus()
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault()
          first?.focus()
        }
      }
    }

    document.addEventListener('keydown', handleKey)
    return () => document.removeEventListener('keydown', handleKey)
  }, [isOpen])

  const onSubmit = (data: CreatePostSchema) => {
    setApiError(null)
    createPost(data, {
      onSuccess: () => {
        reset()
        onClose()
      },
      onError: (err: any) => {
        const msg = err?.response?.data?.detail || err?.message || 'Failed to create post'
        setApiError(typeof msg === 'string' ? msg : JSON.stringify(msg))
      },
    })
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="create-post-title"
        ref={containerRef}
        className="bg-white rounded shadow-lg p-6 w-full max-w-md"
      >
        <div className="flex items-center justify-between">
          <h2 id="create-post-title" className="text-lg font-semibold mb-4">Create Achievement</h2>
          <button
            aria-label="Close modal"
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 ml-2"
          >
            ×
          </button>
        </div>
        {apiError && <div className="text-sm text-red-600 mb-3">{apiError}</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
          <div>
            <label className="block text-sm font-medium">Title *</label>
            <input
              className="w-full border p-2 rounded text-sm"
              placeholder="Your achievement title"
              {...register('title')}
              autoFocus
            />
            {formState.errors.title && <span className="text-xs text-red-600">{formState.errors.title.message}</span>}
          </div>
          <div>
            <label className="block text-sm font-medium">Description *</label>
            <textarea
              className="w-full border p-2 rounded text-sm"
              placeholder="Tell your story"
              rows={4}
              {...register('description')}
            />
            {formState.errors.description && <span className="text-xs text-red-600">{formState.errors.description.message}</span>}
          </div>
          <div>
            <label className="block text-sm font-medium">Category</label>
            <input
              className="w-full border p-2 rounded text-sm"
              placeholder="e.g., Academic, Skill, Project"
              {...register('category')}
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Image URL (optional)</label>
            <input
              className="w-full border p-2 rounded text-sm"
              placeholder="https://example.com/image.jpg"
              {...register('image')}
            />
            {formState.errors.image && <span className="text-xs text-red-600">{formState.errors.image.message}</span>}
          </div>
          <div className="flex gap-2 justify-end mt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={isPending}
              className="px-4 py-2 border rounded text-sm">
              Cancel
            </button>
            <button
              type="submit"
              disabled={isPending}
              className={`px-4 py-2 rounded text-sm text-white ${isPending ? 'bg-indigo-300' : 'bg-indigo-600'}`}>
              {isPending ? 'Creating...' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
