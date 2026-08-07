import { motion, AnimatePresence } from 'framer-motion'
import { Check, Lock } from 'lucide-react'
import { cn } from '@/lib/utils'

interface VoteOptionProps {
  option: { id: string; text: string; votes?: number }
  totalVotes: number
  isSelected: boolean
  isDisabled: boolean
  onVote: () => void
  index: number
}

export function VoteOption({ option, totalVotes, isSelected, isDisabled, onVote, index }: VoteOptionProps) {
  const percentage = totalVotes > 0 && option.votes !== undefined
    ? (option.votes / totalVotes) * 100
    : 0

  const colors = [
    'from-accent-purple to-primary-500',
    'from-accent-cyan to-cyan-500',
    'from-accent-amber to-amber-500',
    'from-accent-pink to-pink-500',
    'from-accent-emerald to-emerald-500',
    'from-accent-rose to-rose-500',
  ]

  const color = colors[index % colors.length]

  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, type: 'spring', stiffness: 300 }}
      whileHover={isDisabled ? {} : { scale: 1.02, y: -2 }}
      whileTap={isDisabled ? {} : { scale: 0.98 }}
      onClick={onVote}
      disabled={isDisabled}
      className={cn(
        'relative w-full rounded-2xl overflow-hidden border transition-all duration-300',
        isSelected
          ? 'border-emerald-500/50 bg-emerald-500/10'
          : isDisabled
          ? 'border-slate-700/50 bg-slate-800/30 opacity-50 cursor-not-allowed'
          : 'border-white/10 bg-slate-800/40 hover:border-white/20 hover:bg-slate-800/60 cursor-pointer'
      )}
    >
      {/* Background progress bar */}
      {totalVotes > 0 && (
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className={cn('absolute inset-y-0 left-0 bg-gradient-to-r opacity-20', color)}
        />
      )}

      <div className="relative z-10 flex items-center justify-between p-5">
        <div className="flex items-center gap-3">
          <AnimatePresence mode="wait">
            {isSelected ? (
              <motion.div
                key="check"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                exit={{ scale: 0 }}
                className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center"
              >
                <Check className="w-5 h-5 text-white" />
              </motion.div>
            ) : isDisabled ? (
              <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
                <Lock className="w-4 h-4 text-slate-400" />
              </div>
            ) : (
              <div className={cn('w-8 h-8 rounded-full bg-gradient-to-r', color)} />
            )}
          </AnimatePresence>

          <div className="text-left">
            <span className={cn(
              'text-lg font-bold',
              isSelected ? 'text-emerald-400' : 'text-white'
            )}>
              {option.text}
            </span>
            {isSelected && (
              <motion.p
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="text-sm text-emerald-400/80 font-medium"
              >
                Your vote
              </motion.p>
            )}
          </div>
        </div>

        <div className="text-right">
          <span className="text-2xl font-black text-white tabular-nums">
            {option.votes?.toLocaleString() || 0}
          </span>
          <span className="block text-sm text-slate-400">
            {percentage.toFixed(1)}%
          </span>
        </div>
      </div>
    </motion.button>
  )
}