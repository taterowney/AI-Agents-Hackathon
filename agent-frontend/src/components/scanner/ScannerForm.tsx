'use client';

import { useState } from 'react';

export default function ScannerForm() {
  const [isLoading] = useState(false);

  return (
    <div className="glass-panel rounded-xl">
      <div className="p-6">
        <div className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-white/80 mb-2">
              Target URL
            </label>
            <input
              type="text"
              placeholder="https://your-ai-endpoint.com"
              className="input-style w-full h-11 px-4 rounded-lg text-[15px]"
            />
            <p className="mt-2 text-sm text-white/40">
              Enter the endpoint URL of the AI system you want to analyze
            </p>
          </div>

          <button
            className="scan-button w-full h-11 rounded-lg font-medium text-white/90"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <LoadingSpinner />
                <span>Scanning...</span>
              </div>
            ) : (
              'Start Vulnerability Scan'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

function LoadingSpinner() {
  return (
    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
  );
} 