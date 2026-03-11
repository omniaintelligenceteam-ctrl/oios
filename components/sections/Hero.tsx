'use client'

import { ArrowRight } from 'lucide-react'

import { ShimmerText } from '@/components/ui/shimmer-text'
import { SplineScene } from '@/components/ui/splite'
import { TextReveal } from '@/components/ui/text-reveal'

export function Hero() {
  return (
    <section className="section-shell relative z-10 grid grid-cols-1 gap-10 py-16 lg:grid-cols-2 lg:items-center lg:py-24">
      <div>
        <p className="mb-4 inline-flex rounded-full border border-white/15 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.18em] text-slate-300">
          <ShimmerText>AI-Powered Operations Partner</ShimmerText>
        </p>
        <h1 className="text-4xl font-bold leading-[1.08] text-white sm:text-5xl lg:text-6xl">
          <TextReveal text="Answer Every Call. Capture Every Lead. Run Every Task." />
          <br />
          <span className="gradient-text">
            <TextReveal text="See Everything. 24/7." delay={0.22} />
          </span>
        </h1>
        <p className="mt-6 max-w-xl text-base text-slate-300 sm:text-lg">
          OIOS installs one system that answers calls, automates your back office,
          and gives you a real-time command center for the entire operation.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <a
            href="#pricing"
            className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-amber-500 to-amber-400 px-5 py-3 font-semibold text-white transition hover:brightness-110"
          >
            Book Your Free Audit
            <ArrowRight className="h-4 w-4" />
          </a>
          <a
            href="#command-center"
            className="rounded-lg border border-white/20 px-5 py-3 font-semibold text-slate-200 transition hover:bg-white/10"
          >
            See Command Center
          </a>
        </div>
      </div>

      <div className="glass relative h-[360px] overflow-hidden rounded-2xl sm:h-[460px]">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_25%_25%,rgba(13,148,136,0.2),transparent_45%),radial-gradient(circle_at_80%_70%,rgba(245,158,11,0.14),transparent_45%)]" />
        <SplineScene
          scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode"
          className="h-full w-full"
        />
      </div>
    </section>
  )
}

