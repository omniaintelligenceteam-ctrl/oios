'use client'

import { ScrollReveal } from '@/components/ui/scroll-reveal'

export function Footer() {
  return (
    <footer className="section-shell relative z-10 border-t border-white/10 py-8">
      <ScrollReveal>
        <div className="flex flex-col items-start justify-between gap-3 sm:flex-row sm:items-center">
          <p className="text-sm text-slate-400">Â© {new Date().getFullYear()} OIOS</p>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <a href="mailto:team@getoios.com" className="hover:text-white">
              team@getoios.com
            </a>
            <a href="tel:8667821303" className="hover:text-white">
              8667821303
            </a>
          </div>
        </div>
      </ScrollReveal>
    </footer>
  )
}
