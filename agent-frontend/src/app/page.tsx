"use client"

import { useState } from "react"
import { Lock, Scan } from "lucide-react"

export default function Home() {
  const [loading, setLoading] = useState(false)

  return (
    <main className="min-h-screen p-8 flex flex-col items-center">
      {/* Header */}
      <div className="w-full max-w-3xl mb-2">
        <h1 className="heading-primary">Nexus Shield</h1>
      </div>

      <div className="w-full max-w-3xl mb-16 text-center">
        <h2 className="heading-secondary mb-3">AI Vulnerability Scanner</h2>
        <p className="text-subtle">
          Detect and analyze potential security vulnerabilities in AI systems
        </p>
      </div>

      {/* Main Form */}
      <div className="w-full max-w-[640px] space-y-6">
        <div>
          <label className="input-label">
            <Lock />
            Agent Description
          </label>
          <textarea
            className="input-field h-[120px] resize-none"
            placeholder="Describe the AI agent's purpose, capabilities, and constraints..."
          />
        </div>

        <div>
          <label className="input-label">
            <Scan />
            Agent URL (optional)
          </label>
          <input
            type="text"
            className="input-field"
            placeholder="https://your-ai-endpoint.com"
          />
        </div>

        <button className="scan-button mt-2">
          Initiate Vulnerability Scan
        </button>

        {/* Results Section */}
        <div className="mt-12 pt-8 border-t border-white/[0.08]">
          <h3 className="heading-primary mb-4">Analysis Results</h3>
          <div className="text-subtle">
            Scan results will appear here...
          </div>
        </div>
      </div>
    </main>
  )
}
