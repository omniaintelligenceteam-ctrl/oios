'use client'

import { useEffect, useMemo, useState } from 'react'

import { Activity, Clock3, DollarSign, PhoneCall } from 'lucide-react'

const createData = () =>
  Array.from({ length: 18 }, (_, index) => ({
    x: index,
    value: 24 + Math.sin(index * 0.5) * 10 + Math.random() * 8,
  }))

export function RealTimeAnalytics() {
  const [data, setData] = useState(createData)
  const [activeCalls, setActiveCalls] = useState(6)
  const [bookedToday, setBookedToday] = useState(14)

  useEffect(() => {
    const interval = window.setInterval(() => {
      setData((prev) => {
        const nextValue = 24 + Math.sin(Date.now() / 1000) * 8 + Math.random() * 9
        return [...prev.slice(1), { x: prev[prev.length - 1].x + 1, value: nextValue }]
      })
      setActiveCalls((prev) => Math.max(2, (prev + (Math.random() > 0.5 ? 1 : -1)) % 12))
      setBookedToday((prev) => prev + (Math.random() > 0.72 ? 1 : 0))
    }, 1700)
    return () => window.clearInterval(interval)
  }, [])

  const path = useMemo(() => {
    const width = 620
    const height = 220
    return data
      .map((point, index) => {
        const x = (index / (data.length - 1)) * width
        const y = height - ((point.value - 10) / 40) * height
        return `${index === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`
      })
      .join(' ')
  }, [data])

  return (
    <div className="glass rounded-2xl p-6">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <h3 className="text-xl font-semibold">Command Center Live Feed</h3>
        <span className="inline-flex items-center gap-2 rounded-full border border-teal-400/40 bg-teal-400/15 px-3 py-1 text-xs text-teal-200">
          <Activity className="h-3.5 w-3.5" />
          Real-time
        </span>
      </div>

      <svg viewBox="0 0 620 220" className="h-56 w-full rounded-xl bg-white/[0.02] p-3">
        <path d={path} fill="none" stroke="url(#line)" strokeWidth="3" strokeLinecap="round" />
        <defs>
          <linearGradient id="line" x1="0" y1="0" x2="620" y2="0">
            <stop stopColor="#14b8a6" />
            <stop offset="1" stopColor="#f59e0b" />
          </linearGradient>
        </defs>
      </svg>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
          <p className="text-xs text-slate-400">Active Calls</p>
          <p className="mt-1 flex items-center gap-2 text-lg font-semibold">
            <PhoneCall className="h-4 w-4 text-teal-300" />
            {activeCalls}
          </p>
        </div>
        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
          <p className="text-xs text-slate-400">Booked Today</p>
          <p className="mt-1 flex items-center gap-2 text-lg font-semibold">
            <Clock3 className="h-4 w-4 text-cyan-300" />
            {bookedToday}
          </p>
        </div>
        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
          <p className="text-xs text-slate-400">Pipeline</p>
          <p className="mt-1 flex items-center gap-2 text-lg font-semibold">
            <DollarSign className="h-4 w-4 text-amber-300" />
            $184k
          </p>
        </div>
        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
          <p className="text-xs text-slate-400">Follow-ups</p>
          <p className="mt-1 text-lg font-semibold text-emerald-300">On Track</p>
        </div>
      </div>
    </div>
  )
}

