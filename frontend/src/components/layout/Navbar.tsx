import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Vote, Plus } from 'lucide-react'

export function Navbar() {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-white/[0.06]"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-accent-purple flex items-center justify-center group-hover:shadow-lg group-hover:shadow-primary-500/25 transition-shadow">
              <Vote className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white tracking-tight">
              Vote<span className="text-primary-400">Live</span>
            </span>
          </Link>

          <Link
            to="/create"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500/10 text-primary-400 hover:bg-primary-500/20 border border-primary-500/20 transition-colors text-sm font-medium"
          >
            <Plus className="w-4 h-4" />
            Create Poll
          </Link>
        </div>
      </div>
    </motion.nav>
  )
}