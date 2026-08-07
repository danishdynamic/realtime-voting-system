import { motion } from 'framer-motion'
import { useCountdown } from '@/hooks/useCountdown'
import { Timer, AlertCircle } from 'lucide-react'

interface CountdownTimerProps {
  endTime: string
}

export function CountdownTimer({ endTime }: CountdownTimerProps) {
  const { formatted, expired, totalSeconds } = useCountdown(endTime)

  const isUrgent = totalSeconds < 300 && !expired // Less than 5 minutes

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`rounded-2xl p-5 text-center border ${
        expired
          ? 'bg-red-500/10 border-red-500/20'
          : isUrgent
          ? 'bg-amber-500/10 border-amber-500/20'
          : 'bg-emerald-500/10 border-emerald-500/20'
      }`}
    >
      <div className="flex items-center justify-center gap-2 mb-2">
        {expired ? (
          <AlertCircle className="w-5 h-5 text-red-400" />
        ) : (
          <Timer className={`w-5 h-5 ${isUrgent ? 'text-amber-400' : 'text-emerald-400'}`} />
        )}
        <span className={`text-sm font-semibold uppercase tracking-wider ${
          expired ? 'text-red-400' : isUrgent ? 'text-amber-400' : 'text-emerald-400'
        }`}>
          {expired ? 'Voting Closed' : isUrgent ? 'Ending Soon' : 'Time Remaining'}
        </span>
      </div>

      {expired ? (
        <p className="text-2xl font-black text-red-400">POLL ENDED</p>
      ) : (
        <motion.p
          key={formatted}
          initial={{ y: -5, opacity: 0.5 }}
          animate={{ y: 0, opacity: 1 }}
          className={`text-4xl font-black font-mono tracking-wider ${
            isUrgent ? 'text-amber-400' : 'text-emerald-400'
          }`}
        >
          {formatted}
        </motion.p>
      )}
    </motion.div>
  )
}