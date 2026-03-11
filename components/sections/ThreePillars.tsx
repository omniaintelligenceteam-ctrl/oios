import { LayoutDashboard, PhoneCall, Workflow } from 'lucide-react'

import { SpotlightCard } from '@/components/ui/spotlight-card'

const pillars = [
  {
    title: 'AI Receptionist',
    icon: PhoneCall,
    glow: 'rgba(45, 212, 191, 0.24)',
    points: ['24/7 call answering', 'Lead capture + scoring', 'Booking on your calendar'],
  },
  {
    title: 'AI Back Office',
    icon: Workflow,
    glow: 'rgba(245, 158, 11, 0.22)',
    points: ['Proposals in seconds', 'Automated follow-up sequences', 'CRM updates without typing'],
  },
  {
    title: 'AI Command Center',
    icon: LayoutDashboard,
    glow: 'rgba(56, 189, 248, 0.24)',
    points: ['Pipeline health snapshots', 'Revenue and response tracking', 'Daily owner briefing'],
  },
]

export function ThreePillars() {
  return (
    <section id="pillars" className="section-shell relative z-10 py-16">
      <p className="mb-3 text-xs uppercase tracking-[0.2em] text-teal-300">Three Pillars</p>
      <h2 className="max-w-3xl text-3xl font-bold text-white sm:text-4xl">
        Built to Monitor, Build, Automate, and Run Your Operation
      </h2>
      <div className="mt-8 grid gap-4 md:grid-cols-3">
        {pillars.map((pillar) => {
          const Icon = pillar.icon
          return (
            <SpotlightCard key={pillar.title} glowColor={pillar.glow}>
              <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg border border-white/15 bg-white/5">
                <Icon className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white">{pillar.title}</h3>
              <ul className="mt-4 space-y-2">
                {pillar.points.map((point) => (
                  <li key={point} className="text-sm text-slate-300">
                    {point}
                  </li>
                ))}
              </ul>
            </SpotlightCard>
          )
        })}
      </div>
    </section>
  )
}

