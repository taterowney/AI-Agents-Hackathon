import { Shield } from '@phosphor-icons/react'

export function LoadingSpinner() {
  return (
    <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  )
}

export function FuturisticLoader() {
  return (
    <div className="relative">
      <div className="absolute -inset-8 bg-gradient-to-r from-red-500 to-purple-500 rounded-full opacity-20 blur-lg animate-pulse"></div>
      <div className="relative flex items-center justify-center">
        <div className="absolute h-24 w-24 border-2 border-red-500/20 rounded-full animate-ping"></div>
        <div className="absolute h-24 w-24 border-2 border-purple-500/40 rounded-full animate-pulse"></div>
        <div
          className="absolute h-16 w-16 border border-red-500/60 rounded-full animate-spin"
          style={{ animationDuration: "3s" }}
        ></div>
        <div className="h-12 w-12 bg-gradient-to-br from-red-500 to-purple-600 rounded-full flex items-center justify-center">
          <Shield className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  )
} 