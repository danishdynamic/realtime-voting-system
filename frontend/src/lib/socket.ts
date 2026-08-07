import { io } from 'socket.io-client'

const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:8000'

export const socket = io(WS_URL, {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
})

export function subscribeToPoll(pollId: string, callback: (data: { poll_id: string; results: Record<string, number> }) => void) {
  const handler = (data: { poll_id: string; results: Record<string, number> }) => {
    if (data.poll_id === pollId) callback(data)
  }
  socket.on('vote_update', handler)
  return () => socket.off('vote_update', handler)
}
