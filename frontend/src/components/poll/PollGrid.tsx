import { PollCard } from './PollCard'
import type { Poll } from '@/types/poll'

interface PollGridProps {
  polls: Poll[]
  title: string
}

export function PollGrid({ polls, title }: PollGridProps) {
  if (polls.length === 0) return null

  return (
    <section className="mb-10">
      <h2 className="text-xl font-bold text-white mb-5 flex items-center gap-2">
        {title}
        <span className="text-sm font-normal text-slate-500">({polls.length})</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {polls.map((poll, i) => (
          <PollCard key={poll.poll_id} poll={poll} index={i} />
        ))}
      </div>
    </section>
  )
}