'use client'

import { CheckCircle2 } from 'lucide-react'

import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { ShimmerText } from '@/components/ui/shimmer-text'

const features = [
  'AI receptionist setup + call handling',
  'Back-office automation playbooks',
  'Command center dashboard + daily reporting',
  'CRM/workflow integration + launch support',
  'Weekly optimization and improvement cycle',
]

export function Pricing() {
  return (
    <section id="pricing" className="section-shell relative z-10 py-16">
      <ScrollReveal>
        <div className="glass mx-auto max-w-4xl rounded-2xl p-7 sm:p-9">
          <p className="mb-3 text-xs uppercase tracking-[0.2em] text-amber-300">
            <ShimmerText>Founding Member Offer</ShimmerText>
          </p>
          <h2 className="text-3xl font-bold text-white sm:text-4xl">$2,000 / Month</h2>
          <p className="mt-3 text-slate-300">
            3-week rollout. 60-day satisfaction guarantee. Limited founding member spots.
          </p>
          <div className="mt-7 grid gap-3 sm:grid-cols-2">
            {features.map((feature, index) => (
              <ScrollReveal key={feature} delay={index * 0.08}>
                <div className="flex items-start gap-2 rounded-lg border border-white/10 p-3">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 text-emerald-300" />
                  <p className="text-sm text-slate-300">{feature}</p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </ScrollReveal>
    </section>
  )
}
