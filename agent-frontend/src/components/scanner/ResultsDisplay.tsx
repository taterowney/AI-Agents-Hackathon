'use client';

export default function ResultsDisplay() {
  return (
    <div className="glass-panel rounded-xl overflow-hidden">
      <div className="p-8">
        <h2 className="text-lg font-medium mb-6 flex items-center gap-3">
          <span className="w-2 h-2 rounded-full bg-red-500" />
          Analysis Results
        </h2>
        
        <div className="space-y-4 text-[15px] text-white/60">
          <p>Scan results will appear here...</p>
        </div>
      </div>
    </div>
  );
} 