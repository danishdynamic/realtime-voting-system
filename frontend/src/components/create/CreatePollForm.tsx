import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, X, Clock, Type, List, User } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { createPoll } from '@/lib/api'
import { toast } from 'sonner'

export function CreatePollForm() {
  const navigate = useNavigate()
  const [question, setQuestion] = useState('')
  const [options, setOptions] = useState(['', ''])
  const [createdBy, setCreatedBy] = useState('')
  const [durationMinutes, setDurationMinutes] = useState(30)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const addOption = () => {
    if (options.length < 6) setOptions([...options, ''])
  }

  const removeOption = (index: number) => {
    if (options.length > 2) {
      setOptions(options.filter((_, i) => i !== index))
    }
  }

  const updateOption = (index: number, value: string) => {
    const newOptions = [...options]
    newOptions[index] = value
    setOptions(newOptions)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const validOptions = options.filter(o => o.trim())
    if (validOptions.length < 2) {
      toast.error('Please provide at least 2 options')
      return
    }

    setIsSubmitting(true)
    try {
      const now = new Date()
      const startTime = new Date(now.getTime() + 1000)
      const endTime = new Date(now.getTime() + durationMinutes * 60000)

      const data = await createPoll({
        question: question.trim(),
        options: validOptions,
        created_by: createdBy.trim() || 'Anonymous',
        start_time: startTime.toISOString(),
        end_time: endTime.toISOString(),
      })

      toast.success('Poll created successfully!')
      navigate(`/poll/${data.poll_id}`)
    } catch (err) {
      toast.error('Failed to create poll')
      console.error(err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto"
    >
      <Card className="p-8">
        <h1 className="text-3xl font-black text-white mb-2">Create a Poll</h1>
        <p className="text-slate-400 mb-8">Set up your question, options, and voting duration.</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Question */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-slate-300 mb-2">
              <Type className="w-4 h-4 text-primary-400" />
              Question
            </label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Apple vs Orange - Which is better?"
              required
              className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/50 focus:ring-2 focus:ring-primary-500/20 transition-all"
            />
          </div>

          {/* Options */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-slate-300 mb-2">
              <List className="w-4 h-4 text-primary-400" />
              Options
            </label>
            <div className="space-y-3">
              <AnimatePresence>
                {options.map((option, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 10 }}
                    className="flex items-center gap-2"
                  >
                    <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center text-slate-500 font-bold text-sm">
                      {String.fromCharCode(65 + index)}
                    </div>
                    <input
                      type="text"
                      value={option}
                      onChange={(e) => updateOption(index, e.target.value)}
                      placeholder={`Option ${index + 1}`}
                      required
                      className="flex-1 px-4 py-2.5 rounded-xl bg-slate-800/50 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/50 focus:ring-2 focus:ring-primary-500/20 transition-all"
                    />
                    {options.length > 2 && (
                      <button
                        type="button"
                        onClick={() => removeOption(index)}
                        className="p-2 rounded-lg hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>

              {options.length < 6 && (
                <button
                  type="button"
                  onClick={addOption}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-dashed border-white/20 text-slate-400 hover:text-white hover:border-white/40 transition-colors text-sm font-medium"
                >
                  <Plus className="w-4 h-4" />
                  Add Option
                </button>
              )}
            </div>
          </div>

          {/* Duration & Creator */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-semibold text-slate-300 mb-2">
                <Clock className="w-4 h-4 text-primary-400" />
                Duration
              </label>
              <select
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(Number(e.target.value))}
                className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 text-white focus:outline-none focus:border-primary-500/50 focus:ring-2 focus:ring-primary-500/20 transition-all"
              >
                <option value={5}>5 minutes</option>
                <option value={15}>15 minutes</option>
                <option value={30}>30 minutes</option>
                <option value={60}>1 hour</option>
                <option value={120}>2 hours</option>
                <option value={1440}>24 hours</option>
              </select>
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-semibold text-slate-300 mb-2">
                <User className="w-4 h-4 text-primary-400" />
                Created By
              </label>
              <input
                type="text"
                value={createdBy}
                onChange={(e) => setCreatedBy(e.target.value)}
                placeholder="Your name (optional)"
                className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/50 focus:ring-2 focus:ring-primary-500/20 transition-all"
              />
            </div>
          </div>

          {/* Submit */}
          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full"
            isLoading={isSubmitting}
          >
            Create Poll
          </Button>
        </form>
      </Card>
    </motion.div>
  )
}