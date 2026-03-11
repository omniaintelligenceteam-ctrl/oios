import { InteractiveAccordion } from '@/components/ui/interactive-accordion'

const items = [
  {
    question: 'How fast can OIOS go live?',
    answer:
      'Most implementations are live in about 3 weeks, including call flows, automation playbooks, and dashboard setup.',
  },
  {
    question: 'Will this replace my current team?',
    answer:
      'No. OIOS takes repetitive admin and response tasks off your team so they can focus on sales, service quality, and customer experience.',
  },
  {
    question: 'Can OIOS work with our current CRM and tools?',
    answer:
      'Yes. OIOS is designed to integrate with common CRMs, scheduling tools, and communication systems used by service businesses.',
  },
  {
    question: 'What if we are not seeing results?',
    answer:
      'Founding members include a 60-day satisfaction guarantee and weekly optimization so workflows keep improving from real usage data.',
  },
]

export function FAQ() {
  return (
    <section id="faq" className="section-shell relative z-10 py-16">
      <p className="mb-3 text-xs uppercase tracking-[0.2em] text-cyan-300">FAQ</p>
      <h2 className="mb-7 text-3xl font-bold text-white sm:text-4xl">Questions, Answered</h2>
      <InteractiveAccordion items={items} />
    </section>
  )
}

