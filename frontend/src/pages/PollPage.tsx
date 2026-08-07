import { useParams } from 'react-router-dom'
import { useEffect, useState } from "react"; 
import { motion, AnimatePresence } from 'framer-motion'
import { usePoll } from '@/hooks/usePoll'
import { useVote } from '@/hooks/useVote'
import { CountdownTimer } from '@/components/poll/CountdownTimer'
import { VoteOption } from '@/components/poll/VoteOption'
import { WinnerBanner } from '@/components/poll/WinnerBanner'
import { LiveCounter } from '@/components/poll/LiveCounter'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { Link } from 'react-router-dom'
import { ArrowLeft, Vote, AlertCircle, Loader2 } from 'lucide-react'
import { Toaster, toast } from 'sonner'

export function PollPage() {
  const { pollId } = useParams<{ pollId: string }>()
  const { poll, isLoading } = usePoll(pollId!)
  const { vote, isVoting, voteError } = useVote(pollId!)
 

  // Show vote error toast
  useEffect(() => {
    if (voteError) toast.error(voteError)
  }, [voteError])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <Loader2 className="w-10 h-10 text-primary-400 animate-spin" />
      </div>
    )
  }

  if (!poll) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <Card className="p-8 text-center">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Poll Not Found</h2>
          <p className="text-slate-400 mb-6">This poll doesn't exist or has been removed.</p>
          <Link to="/">
            <Button variant="ghost" className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Button>
          </Link>
        </Card>
      </div>
    )
  }

  const isExpired = poll.status === 'ended'
  const totalVotes = poll.results
    ? Object.values(poll.results).reduce((a, b) => a + b, 0)
    : 0

  return (
    <div className="min-h-screen bg-slate-950 pt-24 pb-12 px-4">
      <Toaster position="top-center" richColors />

      <div className="max-w-2xl mx-auto">
        {/* Back Link */}
        <Link to="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-6">
          <ArrowLeft className="w-4 h-4" />
          Back to polls
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Header */}
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', delay: 0.1 }}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-xs font-bold uppercase tracking-wider mb-4"
            >
              <Vote className="w-3.5 h-3.5" />
              Poll
            </motion.div>
            <h1 className="text-3xl sm:text-4xl font-black text-white mb-2">
              {poll.question}
            </h1>
            <p className="text-slate-400">
              <LiveCounter value={totalVotes} /> total votes
            </p>
          </div>

          {/* Countdown */}
          <CountdownTimer endTime={poll.end_time} />

          {/* Winner Banner (if ended) */}
          <AnimatePresence>
            {isExpired && <WinnerBanner poll={poll} />}
          </AnimatePresence>

          {/* Vote Options */}
          {!isExpired && (
            <Card className="p-6">
              <h3 className="text-lg font-bold text-white mb-4">Cast Your Vote</h3>
              <div className="space-y-3">
                {poll.options?.map((option, index) => (
                  <VoteOption
                    key={option.id}
                    option={{
                      ...option,
                      votes: poll.results?.[option.text] || 0,
                    }}
                    totalVotes={totalVotes}
                    isSelected={poll.userVote === option.text}
                    isDisabled={!!poll.userVote || isVoting}
                    onVote={() => vote(option.id, option.text)}
                    index={index}
                  />
                ))}
              </div>

              {poll.userVote && (
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center text-emerald-400 font-semibold mt-4"
                >
                  ✅ You've voted! Watch the results update live.
                </motion.p>
              )}
            </Card>
          )}

          {/* Results only (if ended) */}
          {isExpired && (
            <Card className="p-6">
              <h3 className="text-lg font-bold text-white mb-4">Final Results</h3>
              <div className="space-y-3">
                {poll.options?.map((option, index) => {
                  const votes = poll.results?.[option.text] || 0
                  const percentage = totalVotes > 0 ? (votes / totalVotes) * 100 : 0
                  return (
                    <div key={option.id} className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50">
                      <span className="font-semibold text-white">{option.text}</span>
                      <div className="text-right">
                        <span className="text-white font-bold">{votes.toLocaleString()}</span>
                        <span className="text-slate-500 text-sm ml-2">({percentage.toFixed(1)}%)</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </Card>
          )}
        </motion.div>
      </div>
    </div>
  )
}