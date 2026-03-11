import { AlertTriangle } from 'lucide-react'

const painPoints = [
  'Calls go to voicemail after hours and on busy days.',
  'Follow-ups slip through cracks when the team gets overloaded.',
  'Quotes and paperwork block owner time every afternoon.',
  'No clear live view of leads, jobs, and conversion rate.',
]

export function PainPoints() {
  return (
    <section className="section-shell relative z-10 py-16">
      <div className="mb-8 max-w-2xl">
        <p className="mb-3 text-xs uppercase tracking-[0.2em] text-rose-300">Pain Points</p>
        <h2 className="text-3xl font-bold text-white sm:text-4xl">Sound Familiar?</h2>
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        {painPoints.map((item) => (
          <div key={item} className="glass flex items-start gap-3 rounded-xl p-4">
            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-rose-300" />
            <p className="text-slate-300">{item}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

