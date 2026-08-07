import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDuration(totalSeconds: number): string {
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60

  if (hours > 0) {
    return `${hours}h ${minutes}m`
  }
  if (minutes > 0) {
    return `${minutes}m ${seconds}s`
  }
  return `${seconds}s`
}

export function getWinner(results: Record<string, number>): { names: string[]; votes: number } | null {
  if (!results || Object.keys(results).length === 0) return null
  const entries = Object.entries(results)
  const maxVotes = Math.max(...entries.map(([, v]) => v))
  const winners = entries.filter(([, v]) => v === maxVotes)
  return { names: winners.map(([k]) => k), votes: maxVotes }
}