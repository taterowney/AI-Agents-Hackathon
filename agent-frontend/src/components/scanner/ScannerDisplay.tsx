'use client';

import { useState } from 'react';

type ScanStatus = 'idle' | 'scanning' | 'complete' | 'error';

export default function ScannerDisplay() {
  const [status, setStatus] = useState<string>('idle');

  /* Status setter for future use */

  return (
    <div className="gradient-border p-6 h-full flex flex-col gap-6">
      <h2 className="text-xl font-semibold">Vulnerability Scanner</h2>

      {/* Status Display */}
      <div className="flex items-center gap-3">
        <div className={`w-2.5 h-2.5 rounded-full ${
          status === 'scanning' ? 'bg-yellow-500 animate-pulse' :
          status === 'complete' ? 'bg-green-500' :
          status === 'error' ? 'bg-red-500' :
          'bg-gray-500'
        }`} />
        <span className="text-sm text-white/70">
          {status === 'scanning' ? 'Scanning in progress...' :
           status === 'complete' ? 'Scan complete' :
           status === 'error' ? 'Error during scan' :
           'Ready to scan'}
        </span>
      </div>

      {/* Scanner Animation */}
      <div className="relative h-40 bg-black/20 rounded-lg overflow-hidden">
        <div className={`absolute inset-0 bg-gradient-to-b from-accent-red/10 to-accent-purple/10 ${
          status === 'scanning' ? 'animate-pulse' : ''
        }`}>
          <div className="absolute inset-0 backdrop-blur-sm" />
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <svg className="w-12 h-12 text-white/30" viewBox="0 0 24 24" fill="none">
            <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" strokeWidth="2"/>
            <path d="M3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z" stroke="currentColor" strokeWidth="2"/>
          </svg>
        </div>
      </div>

      {/* Results Area */}
      <div className="flex-1 space-y-4">
        <h3 className="text-sm font-medium text-white/70">Analysis Results</h3>
        <div className="input-field p-4 h-[calc(100%-2rem)] min-h-[200px]">
          {status === 'idle' && (
            <p className="text-white/50">Scan results will appear here...</p>
          )}
          {status === 'scanning' && (
            <div className="space-y-2 animate-pulse">
              <div className="h-4 bg-white/5 rounded w-3/4" />
              <div className="h-4 bg-white/5 rounded w-1/2" />
              <div className="h-4 bg-white/5 rounded w-2/3" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 