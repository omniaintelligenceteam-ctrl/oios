'use client'

import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { ShimmerText } from '@/components/ui/shimmer-text'

const quotes = [
  {
    name: 'Owner, HVAC Company',
    quote:
      'We stopped bleeding after-hours leads within week one. OIOS changed our response speed overnight.',
  },
  {
    name: 'Owner, Electrical Team',
    quote:
      'The back-office automations gave me 12+ hours back each week. It feels like adding two team members.',
  },
  {
    name: 'Owner, Plumbing Business',
    quote:
      'The command center is now where we run our daily standup. Everyone knows what to do and why.',
  },
]

export function Testimonials() {
  return (
    <section className="section-shell relative z-10 py-16">
      <ScrollReveal>
        <p className="mb-3 text-xs uppercase tracking-[0.2em] text-teal-300">Social Proof</p>
        <h2 className="text-3xl font-bold text-white sm:text-4xl">
          What Founding Members Are Saying
        </h2>
        <p className="mt-2 text-sm text-slate-300">
          <ShimmerText>Early implementation cohort feedback</ShimmerText>
        </p>
      </ScrollReveal>
      <div className="mt-8 grid gap-4 md:grid-cols-3">
        {quotes.map((item, index) => (
          <ScrollReveal key={item.name} delay={index * 0.1}>
            <div className="glass rounded-xl p-5">
              <p className="text-sm leading-relaxed text-slate-300">â€œ{item.quote}â€</p>
              <p className="mt-4 text-xs uppercase tracking-[0.14em] text-slate-400">
                {item.name}
              </p>
            </div>
          </ScrollReveal>
        ))}
      </div>
    </section>
  )
}
