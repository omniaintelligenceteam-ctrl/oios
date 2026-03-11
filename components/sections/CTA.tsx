import { Mail, Phone } from 'lucide-react'

import { NeonFlow } from '@/components/ui/neon-flow'
import { ShimmerText } from '@/components/ui/shimmer-text'

export function CTA() {
  return (
    <section id="cta" className="section-shell relative z-10 py-16">
      <div className="glass relative overflow-hidden rounded-2xl p-8 sm:p-12">
        <NeonFlow className="pointer-events-none absolute inset-0 opacity-90" />
        <div className="relative z-10 mx-auto max-w-3xl text-center">
          <p className="mb-3 text-xs uppercase tracking-[0.2em] text-slate-200">
            <ShimmerText>Only 10 founding member spots</ShimmerText>
          </p>
          <h2 className="text-3xl font-bold text-white sm:text-5xl">
            Ready to Stop Leaving Revenue on the Table?
          </h2>
          <p className="mt-4 text-slate-300">
            OIOS is built for service operators who want the speed of AI with the
            control of a real operations system.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <a
              className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-teal-500 to-cyan-500 px-5 py-3 font-semibold text-white"
              href="mailto:team@getoios.com"
            >
              <Mail className="h-4 w-4" />
              team@getoios.com
            </a>
            <a
              className="inline-flex items-center gap-2 rounded-lg border border-white/20 px-5 py-3 font-semibold text-white"
              href="tel:8667821303"
            >
              <Phone className="h-4 w-4" />
              8667821303
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

