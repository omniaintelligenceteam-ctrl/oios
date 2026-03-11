'use client'

import { ArrowRight } from 'lucide-react'

import { AnimatedCounter } from '@/components/ui/animated-counter'
import { ScrollReveal } from '@/components/ui/scroll-reveal'
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
        <div className="mt-8 flex flex-wrap gap-6">
          <ScrollReveal delay={0}>
            <div>
              <p className="text-2xl font-bold text-white">
                <AnimatedCounter value={98} suffix="%" />
              </p>
              <p className="mt-1 text-xs uppercase tracking-[0.12em] text-slate-400">
                Calls Answered
              </p>
            </div>
          </ScrollReveal>
          <ScrollReveal delay={0.1}>
            <div>
              <p className="text-2xl font-bold text-white">
                <AnimatedCounter value={15} suffix="+" />
              </p>
              <p className="mt-1 text-xs uppercase tracking-[0.12em] text-slate-400">
                Hours Saved / Week
              </p>
            </div>
          </ScrollReveal>
          <ScrollReveal delay={0.2}>
            <div>
              <p className="text-2xl font-bold text-white">
                <AnimatedCounter value={3} suffix="x" />
              </p>
              <p className="mt-1 text-xs uppercase tracking-[0.12em] text-slate-400">
                Average ROI
              </p>
            </div>
          </ScrollReveal>
        </div>
      </div>

      <div className="glass relative h-[360px] overflow-hidden rounded-2xl sm:h-[460px] animate-float">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_25%_25%,rgba(13,148,136,0.2),transparent_45%),radial-gradient(circle_at_80%_70%,rgba(245,158,11,0.14),transparent_45%)]" />
        <SplineScene
          scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode"
          className="h-full w-full"
        />
      </div>
    </section>
  )
}
