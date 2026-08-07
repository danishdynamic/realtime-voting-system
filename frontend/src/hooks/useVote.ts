import { useState, useCallback } from 'react'
import { usePollStore } from '@/store/pollStore'
import { castVote } from '@/lib/api'
import confetti from 'canvas-confetti'

export function useVote(pollId: string) {
  const { setUserVote } = usePollStore()
  const [isVoting, setIsVoting] = useState(false)
  const [voteError, setVoteError] = useState<string | null>(null)

  const vote = useCallback(async (optionId: string, optionText: string) => {
    setIsVoting(true)
    setVoteError(null)
    try {
      await castVote(pollId, optionId, optionText)
      setUserVote(pollId, optionText)

      // Trigger confetti
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#8b5cf6', '#06b6d4', '#f59e0b', '#ec4899', '#10b981'],
      })

      return true
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to cast vote'
      setVoteError(message)
      return false
    } finally {
      setIsVoting(false)
    }
  }, [pollId, setUserVote])

  return { vote, isVoting, voteError }
}