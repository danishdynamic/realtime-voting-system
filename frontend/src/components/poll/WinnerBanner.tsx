import { motion } from 'framer-motion'
import { Trophy, Crown, XCircle } from 'lucide-react'
import { getWinner } from '@/lib/utils'
import type { Poll } from '@/types/poll'

interface WinnerBannerProps {
  poll: Poll
}

export function WinnerBanner({ poll }: WinnerBannerProps) {
  const winner = poll.results ? getWinner(poll.results) : null
  if (!winner) return null

  const isTie = winner.names.length > 1

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}
      className="rounded-2xl overflow-hidden border border-amber-500/30"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 p-6 text-center border-b border-amber-500/20">
        <motion.div
          initial={{ rotate: -20, scale: 0 }}
          animate={{ rotate: 0, scale: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
          className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 mb-3 shadow-lg shadow-amber-500/25"
        >
          <Trophy className="w-8 h-8 text-white" />
        </motion.div>
        <h2 className="text-2xl font-black text-white">
          {isTie ? "It's a Tie!" : `${winner.names[0]} Wins!`}
        </h2>
        <p className="text-amber-400/80 mt-1">
          {winner.votes.toLocaleString()} votes
        </p>
      </div>

      {/* Results list */}
      <div className="p-4 space-y-2">
        {poll.options?.map((option) => {
          const votes = poll.results?.[option.text] || 0
          const isWinner = winner.names.includes(option.text)
          const total = Object.values(poll.results || {}).reduce((a, b) => a + b, 0)
          const percentage = total > 0 ? (votes / total) * 100 : 0

          return (
            <motion.div
              key={option.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className={`flex items-center justify-between p-3 rounded-xl ${
                isWinner
                  ? 'bg-emerald-500/10 border border-emerald-500/30'
                  : 'bg-slate-800/50 border border-slate-700/30'
              }`}
            >
              <div className="flex items-center gap-3">
                {isWinner ? (
                  <Crown className="w-5 h-5 text-amber-400" />
                ) : (
                  <XCircle className="w-5 h-5 text-slate-500" />
                )}
                <span className={`font-bold ${isWinner ? 'text-emerald-400' : 'text-slate-300'}`}>
                  {option.text}
                </span>
              </div>
              <div className="text-right">
                <span className={`font-bold ${isWinner ? 'text-emerald-400' : 'text-slate-400'}`}>
                  {votes.toLocaleString()}
                </span>
                <span className="text-slate-500 text-sm ml-2">({percentage.toFixed(1)}%)</span>
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}