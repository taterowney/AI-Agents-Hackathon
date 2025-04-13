'use client';

export default function AgentConfigForm() {
  return (
    <div className="gradient-border p-8 h-full">
      <h2 className="text-2xl font-semibold mb-8 bg-gradient-to-r from-red-500 to-purple-500 bg-clip-text text-transparent">
        Target Configuration
      </h2>
      
      <form className="space-y-8">
        <div className="space-y-3">
          <label className="block text-sm font-medium text-white/80">
            Agent URL
          </label>
          <div className="relative">
            <input
              type="text"
              className="input-field w-full px-4 py-3.5 text-[15px] pr-12 bg-[#0c0c0c] 
                         border border-white/10 rounded-xl transition-all duration-200
                         focus:border-purple-500/50 focus:ring-2 focus:ring-purple-500/20"
              placeholder="Enter the AI agent's endpoint URL..."
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
              </svg>
            </div>
          </div>
          <p className="text-xs text-white/50 ml-1">
            The URL where your AI agent is hosted
          </p>
        </div>

        <button 
          type="submit"
          className="scan-button w-full py-4 px-6 rounded-xl text-white font-medium
                     shadow-lg shadow-purple-500/20 hover:shadow-purple-500/30
                     transition-all duration-200 hover:scale-[1.02]
                     flex items-center justify-center gap-2"
        >
          <span>Initiate Vulnerability Scan</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
            <path d="M12 16v-4M12 8h.01" />
          </svg>
        </button>
      </form>
    </div>
  );
} 