import Image from 'next/image'
import { Sparkles } from 'lucide-react'

import { SplineSceneBasic } from '@/components/ui/demo'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <section className="mx-auto grid w-full max-w-7xl grid-cols-1 gap-10 px-6 py-20 lg:grid-cols-2 lg:items-center">
        <div>
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-zinc-700 px-3 py-1 text-xs uppercase tracking-[0.2em] text-zinc-300">
            <Sparkles className="h-3.5 w-3.5" />
            OIOS Hero
          </p>
          <h1 className="text-balance text-4xl font-semibold leading-tight md:text-6xl">
            AI Systems for Service Businesses
          </h1>
          <p className="mt-5 max-w-xl text-zinc-400">
            Replace admin chaos with one command center for calls, scheduling,
            follow-ups, and revenue growth.
          </p>
          <div className="mt-8">
            <Image
              src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1400&q=80"
              alt="Team collaborating with modern software systems"
              width={1400}
              height={900}
              className="h-44 w-full rounded-xl object-cover"
            />
          </div>
        </div>

        <SplineSceneBasic />
      </section>
    </main>
  )
}

