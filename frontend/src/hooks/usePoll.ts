import { useEffect, useState, useCallback } from 'react'
import { usePollStore } from '@/store/pollStore'
import { getPoll, getResults } from '@/lib/api'
import { subscribeToPoll } from '@/lib/socket'
import type { Poll } from '@/types/poll'

export function usePoll(pollId: string) {
  const { activePoll, setActivePoll, updatePollResults, setLoading, setError } = usePollStore()
  const [isLoading, setLocalLoading] = useState(true)

  const fetchPoll = useCallback(async () => {
    setLocalLoading(true)
    setLoading(true)
    try {
      const [pollData, resultsData] = await Promise.all([
        getPoll(pollId),
        getResults(pollId),
      ])
      setActivePoll({ ...pollData, results: resultsData.results })
      setError(null)
    } catch (err) {
      setError('Failed to load poll')
      console.error(err)
    } finally {
      setLocalLoading(false)
      setLoading(false)
    }
  }, [pollId, setActivePoll, setLoading, setError])

  useEffect(() => {
    fetchPoll()
  }, [fetchPoll])

  useEffect(() => {
    const getSocket = subscribeToPoll(pollId, (data) => {
      updatePollResults(pollId, data.results)
    })

    return () => {
      const socket = getSocket()
      socket.disconnect()
    }
  }, [pollId, updatePollResults])

  return { poll: activePoll, isLoading, refetch: fetchPoll }
}