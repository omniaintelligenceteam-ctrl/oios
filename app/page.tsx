import { CTA } from '@/components/sections/CTA'
import { CommandCenter } from '@/components/sections/CommandCenter'
import { FAQ } from '@/components/sections/FAQ'
import { Footer } from '@/components/sections/Footer'
import { Hero } from '@/components/sections/Hero'
import { Navbar } from '@/components/sections/Navbar'
import { PainPoints } from '@/components/sections/PainPoints'
import { Pricing } from '@/components/sections/Pricing'
import { ROICalculator } from '@/components/sections/ROICalculator'
import { Testimonials } from '@/components/sections/Testimonials'
import { ThreePillars } from '@/components/sections/ThreePillars'
import { FlowFieldBackground } from '@/components/ui/flow-field-background'

export default function HomePage() {
  return (
    <main className="relative min-h-screen">
      <FlowFieldBackground className="pointer-events-none fixed inset-0 z-0 opacity-65" />
      <div className="noise-overlay" />
      <div className="relative z-10">
        <Navbar />
        <Hero />
        <PainPoints />
        <ThreePillars />
        <CommandCenter />
        <ROICalculator />
        <Testimonials />
        <Pricing />
        <FAQ />
        <CTA />
        <Footer />
      </div>
    </main>
  )
}
