import type { Metadata } from 'next'

import './globals.css'

export const metadata: Metadata = {
  title: 'OIOS | AI Operations for Service Businesses',
  description:
    'OIOS installs an AI-powered operations system that answers calls, runs follow-ups, and gives you a live command center.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

