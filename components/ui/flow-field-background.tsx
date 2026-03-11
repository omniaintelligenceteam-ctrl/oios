'use client'

import { useEffect, useRef } from 'react'

type FlowFieldBackgroundProps = {
  className?: string
}

type Dot = {
  x: number
  y: number
  vx: number
  vy: number
}

export function FlowFieldBackground({ className }: FlowFieldBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const mouseRef = useRef({ x: -9999, y: -9999 })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dots: Dot[] = []
    let animationFrame = 0
    let width = 0
    let height = 0

    const resize = () => {
      width = window.innerWidth
      height = window.innerHeight
      canvas.width = width
      canvas.height = height

      dots.length = 0
      const count = Math.min(220, Math.floor((width * height) / 18000))
      for (let i = 0; i < count; i += 1) {
        dots.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
        })
      }
    }

    const onMove = (event: MouseEvent) => {
      mouseRef.current = { x: event.clientX, y: event.clientY }
    }

    const onLeave = () => {
      mouseRef.current = { x: -9999, y: -9999 }
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height)
      const { x: mx, y: my } = mouseRef.current

      for (const dot of dots) {
        const dx = dot.x - mx
        const dy = dot.y - my
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 150) {
          const push = (150 - dist) / 150
          dot.vx += (dx / (dist || 1)) * push * 0.04
          dot.vy += (dy / (dist || 1)) * push * 0.04
        }

        dot.x += dot.vx
        dot.y += dot.vy

        dot.vx *= 0.985
        dot.vy *= 0.985

        if (dot.x < 0) dot.x = width
        if (dot.x > width) dot.x = 0
        if (dot.y < 0) dot.y = height
        if (dot.y > height) dot.y = 0

        ctx.beginPath()
        ctx.arc(dot.x, dot.y, 1.2, 0, Math.PI * 2)
        ctx.fillStyle = 'rgba(125, 211, 252, 0.48)'
        ctx.fill()
      }

      for (let i = 0; i < dots.length; i += 1) {
        const a = dots[i]
        for (let j = i + 1; j < dots.length; j += 1) {
          const b = dots[j]
          const dx = a.x - b.x
          const dy = a.y - b.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 90) {
            const alpha = (1 - dist / 90) * 0.14
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.strokeStyle = `rgba(13, 148, 136, ${alpha})`
            ctx.lineWidth = 1
            ctx.stroke()
          }
        }
      }

      animationFrame = window.requestAnimationFrame(render)
    }

    resize()
    render()
    window.addEventListener('resize', resize)
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseleave', onLeave)

    return () => {
      window.cancelAnimationFrame(animationFrame)
      window.removeEventListener('resize', resize)
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseleave', onLeave)
    }
  }, [])

  return <canvas ref={canvasRef} className={className} />
}

