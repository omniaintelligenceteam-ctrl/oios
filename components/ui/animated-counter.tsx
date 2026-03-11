'use client'

import { useEffect, useRef, useState } from 'react'
import { useInView, useReducedMotion, useSpring, useTransform } from 'framer-motion'

interface AnimatedCounterProps {
  value: number
  prefix?: string
  suffix?: string
  duration?: number
}

export function AnimatedCounter({
  value,
  prefix = '',
  suffix = '',
  duration = 1.2,
}: AnimatedCounterProps) {
  const ref = useRef<HTMLSpanElement>(null)
  const isInView = useInView(ref, { once: true, margin: '-40px' })
  const prefersReducedMotion = useReducedMotion()
  const spring = useSpring(0, {
    stiffness: 140 / Math.max(duration, 0.2),
    damping: 24,
  })
  const rounded = useTransform(spring, (latest) => Math.round(latest))
  const [displayValue, setDisplayValue] = useState(0)

  useEffect(() => {
    const unsubscribe = rounded.on('change', (latest) => {
      setDisplayValue(latest)
    })
    return () => unsubscribe()
  }, [rounded])

  useEffect(() => {
    if (prefersReducedMotion) {
      spring.set(value)
      setDisplayValue(Math.round(value))
      return
    }

    if (isInView) {
      spring.set(value)
    }
  }, [isInView, prefersReducedMotion, spring, value])

  return (
    <span ref={ref}>
      {prefix}
      {displayValue.toLocaleString()}
      {suffix}
    </span>
  )
}
