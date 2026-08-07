import { cn } from '@/lib/utils'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'live' | 'upcoming' | 'ended' | 'default'
  className?: string
}

export function Badge({ children, variant = 'default', className }: BadgeProps) {
  const variants = {
    live: 'bg-red-500/15 text-red-400 border-red-500/20',
    upcoming: 'bg-amber-500/15 text-amber-400 border-amber-500/20',
    ended: 'bg-slate-500/15 text-slate-400 border-slate-500/20',
    default: 'bg-primary-500/15 text-primary-400 border-primary-500/20',
  }

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider border',
        variants[variant],
        className
      )}
    >
      {variant === 'live' && (
        <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
      )}
      {children}
    </span>
  )
}