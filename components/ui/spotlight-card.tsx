'use client'

import { useMemo } from 'react'

import { cn } from '@/lib/utils'

type SpotlightCardProps = {
  className?: string
  children: React.ReactNode
  glowColor?: string
}

export function SpotlightCard({
  className,
  children,
  glowColor = 'rgba(20, 184, 166, 0.28)',
}: SpotlightCardProps) {
  const style = useMemo(
    () =>
      ({
        '--spotlight-color': glowColor,
      }) as React.CSSProperties,
    [glowColor],
  )

  const onMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
    const target = event.currentTarget
    const rect = target.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    target.style.setProperty('--spotlight-x', `${x}px`)
    target.style.setProperty('--spotlight-y', `${y}px`)
  }

  return (
    <div
      className={cn(
        'group relative overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035] p-6 backdrop-blur-xl transition duration-300',
        className,
      )}
      style={style}
      onMouseMove={onMouseMove}
    >
      <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
        <div
          className="absolute h-40 w-40 -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl"
          style={{
            left: 'var(--spotlight-x)',
            top: 'var(--spotlight-y)',
            background: 'var(--spotlight-color)',
          }}
        />
      </div>
      <div className="relative z-10">{children}</div>
    </div>
  )
}

