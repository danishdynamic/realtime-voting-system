import { useState, useEffect, useCallback } from 'react'

interface CountdownState {
  hours: number
  minutes: number
  seconds: number
  totalSeconds: number
  expired: boolean
  formatted: string
}

export function useCountdown(endTime: string): CountdownState {
  const calculateTimeLeft = useCallback((): CountdownState => {
    const now = new Date().getTime()
    const endStr = endTime.endsWith('Z') ? endTime : endTime + 'Z'
    const end = new Date(endStr).getTime()
    const diff = end - now

    if (diff <= 0) {
      return { hours: 0, minutes: 0, seconds: 0, totalSeconds: 0, expired: true, formatted: '00:00:00' }
    }

    const hours = Math.floor(diff / (1000 * 60 * 60))
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    const seconds = Math.floor((diff % (1000 * 60)) / 1000)

    const pad = (n: number) => String(n).padStart(2, '0')
    return {
      hours,
      minutes,
      seconds,
      totalSeconds: Math.floor(diff / 1000),
      expired: false,
      formatted: `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`,
    }
  }, [endTime])

  const [timeLeft, setTimeLeft] = useState<CountdownState>(calculateTimeLeft)

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft())
    }, 1000)

    return () => clearInterval(timer)
  }, [calculateTimeLeft])

  return timeLeft
}