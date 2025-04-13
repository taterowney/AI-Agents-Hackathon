import { motion } from 'framer-motion'
import { Clock, X } from '@phosphor-icons/react'

interface ChatHistory {
  url: string
  timestamp: string
  vulnerabilities: number
}

interface SidebarProps {
  history: ChatHistory[]
  onSelect: (url: string) => void
  onClose: () => void
  isOpen: boolean
}

export function Sidebar({ history, onSelect, onClose, isOpen }: SidebarProps) {
  console.log('Sidebar rendered:', { isOpen, historyLength: history.length })
  return (
    <motion.div
      initial={{ x: -300 }}
      animate={{ x: isOpen ? 0 : -300 }}
      className="fixed left-0 top-0 h-full w-[300px] bg-black/40 backdrop-blur-xl border-r border-white/10 z-50"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/10">
        <span className="text-white/80 text-sm font-medium">Scan History</span>
        <button onClick={onClose} className="text-white/40 hover:text-white/60">
          <X weight="bold" className="w-4 h-4" />
        </button>
      </div>

      {/* History List */}
      <div className="p-4 space-y-2">
        {history.map((item, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => onSelect(item.url)}
            className="w-full p-4 bg-white/5 hover:bg-white/10 rounded-lg transition-all group"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 text-left">
                <p className="text-white/70 text-sm truncate">{item.url}</p>
                <div className="flex items-center gap-2 mt-2">
                  <Clock className="w-3 h-3 text-white/40" />
                  <span className="text-white/40 text-xs">{item.timestamp}</span>
                </div>
              </div>
              <div className="px-2 py-1 bg-red-500/10 rounded text-red-400 text-xs">
                {item.vulnerabilities} found
              </div>
            </div>
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
} 