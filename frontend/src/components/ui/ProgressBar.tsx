import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface ProgressBarProps {
  value: number
  max: number
  color?: string
  label?: string
  showPercentage?: boolean
  className?: string
}

export function ProgressBar({
  value,
  max,
  color = 'from-accent-purple to-primary-500',
  label,
  showPercentage = true,
  className,
}: ProgressBarProps) {
  const percentage = max > 0 ? (value / max) * 100 : 0

  return (
    <div className={cn('w-full', className)}>
      <div className="flex justify-between text-sm mb-1.5">
        <span className="text-slate-300 font-medium">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-slate-400 font-mono">{value.toLocaleString()}</span>
          {showPercentage && (
            <span className="text-slate-500 text-xs">{percentage.toFixed(1)}%</span>
          )}
        </div>
      </div>
      <div className="h-3 bg-slate-800/80 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className={cn('h-full rounded-full bg-gradient-to-r', color)}
        />
      </div>
    </div>
  )
}