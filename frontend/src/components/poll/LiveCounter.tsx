import { motion, AnimatePresence } from 'framer-motion'
import { useState, useEffect, useRef } from 'react'

interface LiveCounterProps {
  value: number
}

export function LiveCounter({ value }: LiveCounterProps) {
  const [displayValue, setDisplayValue] = useState(value)
  const prevValue = useRef(value)

  useEffect(() => {
    if (value !== prevValue.current) {
      setDisplayValue(value)
      prevValue.current = value
    }
  }, [value])

  return (
    <AnimatePresence mode="popLayout">
      <motion.span
        key={displayValue}
        initial={{ y: -10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 10, opacity: 0 }}
        transition={{ duration: 0.2 }}
        className="tabular-nums"
      >
        {displayValue.toLocaleString()}
      </motion.span>
    </AnimatePresence>
  )
}