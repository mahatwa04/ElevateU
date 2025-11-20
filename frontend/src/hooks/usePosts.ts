import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/axios'

export interface Post {
  id: number
  user: string
  title: string
  description: string
  category?: string
  image?: string
  created_at: string
  updated_at: string
  like_count: number
  comment_count: number
}

export interface CreatePostPayload {
  title: string
  description: string
  category?: string
  image?: string
}

export const fetchPosts = async (): Promise<Post[]> => {
  const { data } = await api.get('/api/posts/')
  return data
}

export const createPost = async (payload: CreatePostPayload) => {
  const { data } = await api.post('/api/posts/', payload)
  return data
}

export const usePosts = () => {
  return useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    staleTime: 1000 * 60 * 1,
    retry: 2,
  })
}

export const useCreatePost = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: createPost,
    // Optimistic update: show the new post in the feed immediately while the
    // request is in-flight. On error we rollback to the previous cached value.
    onMutate: async (newPost) => {
      await queryClient.cancelQueries({ queryKey: ['posts'] })

      const previous = queryClient.getQueryData<Post[]>(['posts']) || []

      // Create an optimistic item; negative id to not conflict with server
      const optimistic: Post = {
        id: Date.now() * -1,
        user: 'You',
        title: newPost.title,
        description: newPost.description,
        category: newPost.category || '',
        image: newPost.image || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        like_count: 0,
        comment_count: 0,
      }

      queryClient.setQueryData<Post[]>(['posts'], (old = []) => [optimistic, ...old])

      return { previous }
    },
    onError: (_err, _newPost, context: any) => {
      if (context?.previous) {
        queryClient.setQueryData(['posts'], context.previous)
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] })
    },
  })
}
