"use client"

import { useState } from "react"
import { Space_Grotesk } from 'next/font/google'
import { VulnerabilityResults } from "@/components/VulnerabilityResults"
import { AnimatePresence, motion } from "framer-motion"
import { Input } from "@/components/ui/input"
import { Sidebar } from "@/components/ui/Sidebar"
import { Clock } from '@phosphor-icons/react'
import { supabase } from '@/lib/supabase'

const spaceGrotesk = Space_Grotesk({ subsets: ['latin'] })

export default function Home() {
  const [scanning, setScanning] = useState(false)
  const [agentUrl, setAgentUrl] = useState("")
  const [showResults, setShowResults] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [history, setHistory] = useState([
    {
      url: "https://example-ai.com/api",
      timestamp: "2 hours ago",
      vulnerabilities: 3
    },
    {
      url: "https://test-ai.com/endpoint",
      timestamp: "5 hours ago",
      vulnerabilities: 2
    },
    {
      url: "https://demo-ai.com/chat",
      timestamp: "1 day ago",
      vulnerabilities: 5
    }
  ])
  const [vulnerabilities, setVulnerabilities] = useState<{prompt: string}[]>([])

  const handleKeyPress = async (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && agentUrl) {
      setScanning(true)
      
      try {
        // Fetch vulnerabilities from Supabase
        const { data, error } = await supabase
          .from('vulnerabilities')
          .select('prompt')
          .order('created_at', { ascending: true })

        if (error) throw error

        if (data) {
          setVulnerabilities(data)
          setShowResults(true)
        }
      } catch (error) {
        console.error('Error fetching vulnerabilities:', error)
      } finally {
        setScanning(false)
      }
    }
  }

  return (
    <div className="min-h-screen bg-[#0A0A0F] flex flex-col">
      <Sidebar 
        history={history}
        onSelect={(url) => {
          setAgentUrl(url)
          setIsSidebarOpen(false)
        }}
        onClose={() => setIsSidebarOpen(false)}
        isOpen={isSidebarOpen}
      />
      
      {/* Animated button */}
      <AnimatePresence>
        {!isSidebarOpen && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(true)}
            className="fixed left-6 top-6 p-2 bg-white/5 hover:bg-white/10 rounded-lg transition-all z-50"
          >
            <Clock weight="bold" className="w-5 h-5 text-white/60" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Background effects */}
      <div className="fixed inset-0 bg-gradient-to-b from-[#12121A] via-[#0A0A0F] to-[#080810]" />
      <div className="fixed inset-0">
        <div className="absolute inset-0 stars-small" />
        <div className="absolute inset-0 stars-medium" />
        <div className="absolute inset-0 stars-large" />
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Title at top */}
        <div className="text-center pt-8">
          <h1 className={`text-4xl font-light tracking-[0.2em] text-white/90 ${spaceGrotesk.className}`}>
            SLEEPERAGENT
          </h1>
          <div className="w-full max-w-[200px] h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent mx-auto mt-8" />
        </div>

        {/* Center Circle */}
        <div className="flex-1 flex items-center justify-center -mt-32">
          <div className={`relative ${scanning ? 'scanning' : 'idle-pulse'}`}>
            <div className="circle-container">
              {/* Outer glow layers with conditional opacity */}
              <div className={`absolute inset-[-60px] bg-[#FF3B3B] rounded-full blur-[40px] ${
                scanning ? 'opacity-[0.08]' : 'opacity-[0.15]'
              }`} />
              <div className={`absolute inset-[-40px] bg-[#FF3B3B] rounded-full blur-[30px] ${
                scanning ? 'opacity-[0.12]' : 'opacity-[0.2]'
              }`} />
              <div className={`absolute inset-[-20px] bg-[#FF3B3B] rounded-full blur-[20px] ${
                scanning ? 'opacity-[0.18]' : 'opacity-[0.3]'
              }`} />
              <div className={`absolute inset-[-10px] bg-[#FF3B3B] rounded-full blur-[10px] ${
                scanning ? 'opacity-[0.25]' : 'opacity-[0.4]'
              }`} />
              <div className={`absolute inset-0 bg-[#FF3B3B] rounded-full blur-[5px] ${
                scanning ? 'opacity-[0.3]' : 'opacity-[0.5]'
              }`} />
              
              {/* Static black center with transparency */}
              <div className="relative w-24 h-24">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-white/[0.03] to-transparent animate-[spin_8s_linear_infinite]" />
                <div className="absolute inset-[1px] bg-black/80 rounded-full">
                  <div className="absolute inset-0 rounded-full bg-gradient-to-b from-white/[0.01] to-transparent" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Input and Results Container */}
        <div className="w-full max-w-[800px] mx-auto px-4">
          {/* Input Section */}
          <div className="w-full max-w-[440px] mx-auto mb-8">
            <p className={`
              text-center
              text-sm
              font-medium
              tracking-[0.1em]
              uppercase
              bg-gradient-to-r from-white/60 via-white/80 to-white/60
              bg-clip-text
              text-transparent
              mb-6
              ${spaceGrotesk.className}
            `}>
              {scanning 
                ? "Analyzing System Vulnerabilities" 
                : "Enter AI System Endpoint"
              }
            </p>
            <div className="bg-black/40 backdrop-blur-xl border border-white/5 rounded-2xl p-6">
              <Input
                type="text"
                placeholder="https://your-ai-endpoint.com"
                value={agentUrl}
                onChange={(e) => setAgentUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={scanning}
                className={spaceGrotesk.className}
              />
            </div>
          </div>

          {/* Results Section */}
          <AnimatePresence>
            {showResults && (
              <VulnerabilityResults 
                results={vulnerabilities}
                onClose={() => setShowResults(false)}
              />
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}