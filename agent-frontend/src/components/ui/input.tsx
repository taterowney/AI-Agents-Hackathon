import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-11 w-full rounded-md border",
          "bg-black/30 backdrop-blur-sm",
          "border-white/20",
          "px-3 py-2 text-base",
          "text-white placeholder:text-white/40",
          "focus:border-red-500 focus:ring-red-500/20",
          "hover:bg-black/20",
          "transition-all duration-300",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input } 