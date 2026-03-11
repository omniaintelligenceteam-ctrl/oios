'use client'

type ShimmerTextProps = {
  children: React.ReactNode
  className?: string
}

export function ShimmerText({ children, className = '' }: ShimmerTextProps) {
  return (
    <span
      className={`bg-[length:250%_100%] bg-[linear-gradient(110deg,rgba(244,244,255,0.5)_0%,rgba(255,255,255,0.95)_35%,rgba(244,244,255,0.5)_55%)] bg-clip-text text-transparent animate-[shimmer_2.8s_linear_infinite] ${className}`}
    >
      {children}
    </span>
  )
}

