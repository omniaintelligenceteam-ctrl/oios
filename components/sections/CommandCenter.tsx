'use client'

import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { RealTimeAnalytics } from '@/components/ui/real-time-analytics'

export function CommandCenter() {
  return (
    <section id="command-center" className="section-shell relative z-10 py-16">
      <div className="grid items-start gap-8 lg:grid-cols-[1fr_1.2fr]">
        <ScrollReveal direction="left">
          <div>
            <p className="mb-3 text-xs uppercase tracking-[0.2em] text-cyan-300">
              Command Center
            </p>
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              Live Visibility Without Waiting on Reports
            </h2>
            <p className="mt-4 text-slate-300">
              One screen for open leads, revenue pacing, call volume, and follow-up
              status. Your team sees what matters now and what action is next.
            </p>
          </div>
        </ScrollReveal>
        <ScrollReveal direction="right" delay={0.15}>
          <RealTimeAnalytics />
        </ScrollReveal>
      </div>
    </section>
  )
}
