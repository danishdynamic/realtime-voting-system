import { cn } from '@/lib/utils'
import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  hover?: boolean
}

export function Card({ children, className, hover = false }: CardProps) {
  return (
    <div
      className={cn(
        'bg-slate-850/80 backdrop-blur-xl rounded-2xl border border-white/[0.06]',
        'shadow-xl shadow-black/20',
        hover && 'hover:border-white/10 hover:shadow-2xl hover:shadow-black/30 transition-all duration-300',
        className
      )}
    >
      {children}
    </div>
  )
}