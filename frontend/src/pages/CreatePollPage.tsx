import { CreatePollForm } from '@/components/create/CreatePollForm'
import { motion } from 'framer-motion'
import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export function CreatePollPage() {
  return (
    <div className="min-h-screen bg-slate-950 pt-24 pb-12 px-4">
      <div className="max-w-2xl mx-auto">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to polls
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <CreatePollForm />
        </motion.div>
      </div>
    </div>
  )
}