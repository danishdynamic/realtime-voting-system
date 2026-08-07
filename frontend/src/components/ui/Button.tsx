import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import type { ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'primary' | 'success' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  isLoading?: boolean
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'md',
  className,
  isLoading = false,
}: ButtonProps) {
  const variants = {
    primary: 'bg-gradient-to-r from-primary-600 to-accent-purple text-white hover:shadow-lg hover:shadow-primary-500/25',
    success: 'bg-gradient-to-r from-accent-emerald to-emerald-600 text-white',
    ghost: 'bg-white/5 text-slate-300 hover:bg-white/10 border border-white/10',
    danger: 'bg-gradient-to-r from-accent-rose to-rose-600 text-white',
  }

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  }

  return (
    <motion.button
      whileHover={disabled ? {} : { scale: 1.02 }}
      whileTap={disabled ? {} : { scale: 0.98 }}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={cn(
        'rounded-xl font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className
      )}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          Loading...
        </span>
      ) : (
        children
      )}
    </motion.button>
  )
}