import { create } from 'zustand'
import type { Poll } from '@/types/poll'

interface PollStore {
  polls: Poll[]
  activePoll: Poll | null
  isLoading: boolean
  error: string | null
  setPolls: (polls: Poll[]) => void
  addPoll: (poll: Poll) => void
  setActivePoll: (poll: Poll | null) => void
  updatePollResults: (pollId: string, results: Record<string, number>) => void
  setUserVote: (pollId: string, option: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const usePollStore = create<PollStore>((set) => ({
  polls: [],
  activePoll: null,
  isLoading: false,
  error: null,
  setPolls: (polls) => set({ polls }),
  addPoll: (poll) => set((state) => ({ polls: [poll, ...state.polls] })),
  setActivePoll: (poll) => set({ activePoll: poll }),
  updatePollResults: (pollId, results) => set((state) => ({
    polls: state.polls.map(p =>
      p.poll_id === pollId
        ? { ...p, results: { ...p.results, ...results } }
        : p
    ),
    activePoll: state.activePoll?.poll_id === pollId
      ? { ...state.activePoll, results: { ...state.activePoll.results, ...results } }
      : state.activePoll,
  })),
  setUserVote: (pollId, option) => set((state) => ({
    polls: state.polls.map(p =>
      p.poll_id === pollId ? { ...p, userVote: option } : p
    ),
    activePoll: state.activePoll?.poll_id === pollId
      ? { ...state.activePoll, userVote: option }
      : state.activePoll,
  })),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}))