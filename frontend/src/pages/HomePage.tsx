import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { usePollStore } from '@/store/pollStore'
import { getPolls } from '@/lib/api'
import { PollGrid } from '@/components/poll/PollGrid'
import { Button } from '@/components/ui/Button'
import { Link } from 'react-router-dom'
import { Vote, Sparkles, Loader2 } from 'lucide-react'

export function HomePage() {
  const { polls, setPolls, isLoading, setLoading, error, setError } = usePollStore()
  const [activeTab, setActiveTab] = useState<'all' | 'active' | 'ended'>('all')

  useEffect(() => {
    const fetchPolls = async () => {
      setLoading(true)
      try {
        const data = await getPolls()
        setPolls(data)
        setError(null)
      } catch (err) {
        setError('Failed to load polls')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchPolls()
    const interval = setInterval(fetchPolls, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [setPolls, setLoading, setError])

  const filteredPolls = polls.filter((poll) => {
    if (activeTab === 'active') return poll.status === 'active'
    if (activeTab === 'ended') return poll.status === 'ended'
    return true
  })

  const activePolls = filteredPolls.filter(p => p.status === 'active')
  const upcomingPolls = filteredPolls.filter(p => p.status === 'upcoming')
  const endedPolls = filteredPolls.filter(p => p.status === 'ended')

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Hero Section */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-500/5 to-transparent pointer-events-none" />

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto text-center relative"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-sm font-semibold mb-6"
          >
            <Sparkles className="w-4 h-4" />
            Real-Time Voting Platform
          </motion.div>

          <h1 className="text-5xl sm:text-6xl font-black text-white mb-6 tracking-tight">
            Create Polls.<br />
            <span className="bg-gradient-to-r from-primary-400 via-accent-purple to-accent-cyan bg-clip-text text-transparent">
              Watch Votes Live.
            </span>
          </h1>

          <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
            Create timed polls, share with your audience, and watch results update in real-time. 
            No signup required.
          </p>

          <Link to="/create">
            <Button size="lg" className="gap-2">
              <Vote className="w-5 h-5" />
              Create Your First Poll
            </Button>
          </Link>
        </motion.div>
      </section>

      {/* Polls Section */}
      <section className="max-w-6xl mx-auto px-4 pb-20">
        {/* Tabs */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-1 bg-slate-900/50 rounded-xl p-1 border border-white/[0.06]">
            {(['all', 'active', 'ended'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-sm font-semibold capitalize transition-all ${
                  activeTab === tab
                    ? 'bg-primary-500/20 text-primary-400'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <span className="text-slate-500 text-sm">
            {filteredPolls.length} poll{filteredPolls.length !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="text-center py-20">
            <p className="text-red-400 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()} variant="ghost">
              Retry
            </Button>
          </div>
        )}

        {/* Empty State */}
        {!isLoading && !error && filteredPolls.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20"
          >
            <Vote className="w-16 h-16 text-slate-700 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">No polls yet</h3>
            <p className="text-slate-400 mb-6">Be the first to create a poll!</p>
            <Link to="/create">
              <Button>Create Poll</Button>
            </Link>
          </motion.div>
        )}

        {/* Poll Grids */}
        {!isLoading && !error && (
          <>
            {activePolls.length > 0 && (
              <PollGrid polls={activePolls} title="🔴 Live Now" />
            )}
            {upcomingPolls.length > 0 && (
              <PollGrid polls={upcomingPolls} title="⏳ Starting Soon" />
            )}
            {endedPolls.length > 0 && (
              <PollGrid polls={endedPolls} title="✅ Ended" />
            )}
          </>
        )}
      </section>
    </div>
  )
}