'use client'

import { useRef } from 'react'
import { motion, useInView, useReducedMotion } from 'framer-motion'

interface ScrollRevealProps {
  children: React.ReactNode
  direction?: 'up' | 'down' | 'left' | 'right'
  delay?: number
  duration?: number
  distance?: number
  once?: boolean
  className?: string
}

const directionOffset = {
  up: { x: 0, y: 1 },
  down: { x: 0, y: -1 },
  left: { x: 1, y: 0 },
  right: { x: -1, y: 0 },
}

export function ScrollReveal({
  children,
  direction = 'up',
  delay = 0,
  duration = 0.5,
  distance = 30,
  once = true,
  className,
}: ScrollRevealProps) {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once, margin: '-60px' })
  const prefersReducedMotion = useReducedMotion()

  if (prefersReducedMotion) {
    return <div className={className}>{children}</div>
  }

  const offset = directionOffset[direction]

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, x: offset.x * distance, y: offset.y * distance }}
      animate={isInView ? { opacity: 1, x: 0, y: 0 } : undefined}
      transition={{ duration, delay, ease: 'easeOut' }}
      className={className}
    >
      {children}
    </motion.div>
  )
}
