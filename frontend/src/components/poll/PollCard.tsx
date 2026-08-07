import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Clock, Users, ArrowRight } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import type { Poll } from '@/types/poll'

interface PollCardProps {
  poll: Poll
  index: number
}

export function PollCard({ poll, index }: PollCardProps) {
  
  const totalVotes = poll.total_votes || 0

  const statusVariant = poll.status === 'active' ? 'live' : poll.status === 'upcoming' ? 'upcoming' : 'ended'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
    >
      <Card hover className="p-5 group cursor-pointer">
        <Link to={`/poll/${poll.poll_id}`} className="block">
          <div className="flex items-start justify-between mb-3">
            <Badge variant={statusVariant}>
              {poll.status === 'active' ? 'Live Now' : poll.badge_text || poll.status}
            </Badge>
            <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-primary-400 group-hover:translate-x-1 transition-all" />
          </div>

          <h3 className="text-lg font-bold text-white mb-3 line-clamp-2 group-hover:text-primary-300 transition-colors">
            {poll.question}
          </h3>

          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span className="flex items-center gap-1.5">
              <Users className="w-4 h-4" />
              {totalVotes.toLocaleString()} votes
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4" />
              {poll.options?.length || 0} options
            </span>
          </div>
        </Link>
      </Card>
    </motion.div>
  )
}