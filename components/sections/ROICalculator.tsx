'use client'

import { useMemo, useState } from 'react'

export function ROICalculator() {
  const [callsPerMonth, setCallsPerMonth] = useState(280)
  const [missRate, setMissRate] = useState(22)
  const [closeRate, setCloseRate] = useState(32)
  const [jobValue, setJobValue] = useState(1800)

  const result = useMemo(() => {
    const missedCalls = callsPerMonth * (missRate / 100)
    const recoverableDeals = missedCalls * (closeRate / 100)
    const monthlyRecovered = recoverableDeals * jobValue
    const annualRecovered = monthlyRecovered * 12
    const roiPercent = ((monthlyRecovered - 2000) / 2000) * 100
    return {
      monthlyRecovered,
      annualRecovered,
      roiPercent,
    }
  }, [callsPerMonth, closeRate, jobValue, missRate])

  return (
    <section className="section-shell relative z-10 py-16">
      <div className="glass rounded-2xl p-6 sm:p-8">
        <p className="mb-3 text-xs uppercase tracking-[0.2em] text-amber-300">ROI Snapshot</p>
        <h2 className="text-3xl font-bold text-white sm:text-4xl">
          Estimate What OIOS Recovers in Your Business
        </h2>
        <div className="mt-8 grid gap-7 lg:grid-cols-[1.2fr_1fr]">
          <div className="space-y-5">
            <Slider
              label="Inbound Calls / Month"
              value={callsPerMonth}
              min={80}
              max={600}
              onChange={setCallsPerMonth}
            />
            <Slider
              label="Current Missed Call Rate (%)"
              value={missRate}
              min={5}
              max={45}
              onChange={setMissRate}
            />
            <Slider
              label="Close Rate on Recovered Leads (%)"
              value={closeRate}
              min={10}
              max={60}
              onChange={setCloseRate}
            />
            <Slider
              label="Average Job Value ($)"
              value={jobValue}
              min={500}
              max={5000}
              onChange={setJobValue}
              step={50}
            />
          </div>

          <div className="space-y-3 rounded-xl border border-white/10 bg-white/[0.02] p-5">
            <Metric label="Monthly Revenue Recovered" value={`$${Math.round(result.monthlyRecovered).toLocaleString()}`} />
            <Metric label="Annual Revenue Recovered" value={`$${Math.round(result.annualRecovered).toLocaleString()}`} />
            <Metric label="Estimated ROI vs $2,000/mo" value={`${Math.round(result.roiPercent)}%`} />
          </div>
        </div>
      </div>
    </section>
  )
}

function Slider({
  label,
  value,
  min,
  max,
  onChange,
  step = 1,
}: {
  label: string
  value: number
  min: number
  max: number
  onChange: (value: number) => void
  step?: number
}) {
  return (
    <label className="block">
      <div className="mb-2 flex items-center justify-between text-sm text-slate-300">
        <span>{label}</span>
        <span className="font-semibold text-white">{value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-white/15"
      />
    </label>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-white/10 bg-black/25 p-4">
      <p className="text-xs uppercase tracking-[0.14em] text-slate-400">{label}</p>
      <p className="mt-1 text-2xl font-bold text-white">{value}</p>
    </div>
  )
}

