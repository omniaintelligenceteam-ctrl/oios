'use client'

import { motion } from 'framer-motion'

type NeonFlowProps = {
  className?: string
}

export function NeonFlow({ className }: NeonFlowProps) {
  return (
    <div className={className}>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(13,148,136,0.24),transparent_35%),radial-gradient(circle_at_80%_80%,rgba(245,158,11,0.2),transparent_35%)]" />
      {Array.from({ length: 6 }).map((_, index) => (
        <motion.div
          key={index}
          className="absolute h-[2px] rounded-full"
          style={{
            top: `${16 + index * 14}%`,
            left: index % 2 === 0 ? '-20%' : '10%',
            width: `${40 + index * 8}%`,
            background:
              index % 2 === 0
                ? 'linear-gradient(90deg, transparent, rgba(45,212,191,0.95), transparent)'
                : 'linear-gradient(90deg, transparent, rgba(245,158,11,0.9), transparent)',
            filter: 'blur(0.4px)',
          }}
          animate={{
            x: index % 2 === 0 ? ['0%', '130%'] : ['0%', '-110%'],
            opacity: [0.25, 0.8, 0.25],
          }}
          transition={{
            duration: 9 + index,
            repeat: Infinity,
            ease: 'linear',
            delay: index * 0.45,
          }}
        />
      ))}
    </div>
  )
}

