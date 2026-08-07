import axios from 'axios'
import type { Poll, CreatePollData, VoteEvent } from '@/types/poll'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:5000/api'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Poll APIs
export const getPolls = () => api.get<Poll[]>('/polls').then(r => r.data)
export const getPoll = (id: string) => api.get<Poll>(`/polls/${id}`).then(r => r.data)
export const getResults = (id: string) => api.get<{ poll_id: string; results: Record<string, number> }>(`/polls/${id}/results`).then(r => r.data)
export const createPoll = (data: CreatePollData) => api.post<{ poll_id: string }>('/polls', data).then(r => r.data)

// Vote API
export const castVote = (pollId: string, optionId: string, optionText: string, userId: string = 'anonymous') =>
  api.post(`/polls/${pollId}/vote`, {
    option_id: optionId,
    option_text: optionText,
    user_id: userId,
  }).then(r => r.data)
