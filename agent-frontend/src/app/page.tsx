import AgentConfigForm from '@/components/scanner/AgentConfigForm';
import ScannerDisplay from '@/components/scanner/ScannerDisplay';
import Logo from '@/components/ui/Logo';

export default function Home() {
  return (
    <div className="min-h-screen p-8 flex flex-col gap-8">
      {/* Header with Logo */}
      <header className="flex justify-center mb-8">
        <Logo />
      </header>

      {/* Main Content */}
      <main className="flex flex-col gap-8 max-w-7xl mx-auto w-full">
        <h1 className="text-2xl font-bold text-center text-white/90">
          Advanced AI Vulnerability Detection System
        </h1>
        
        <div className="grid md:grid-cols-2 gap-8">
          {/* Left Panel - Configuration */}
          <AgentConfigForm />
          
          {/* Right Panel - Results */}
          <ScannerDisplay />
        </div>
      </main>
    </div>
  );
}
