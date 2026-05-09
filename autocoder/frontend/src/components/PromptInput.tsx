import React, { useRef } from 'react'
import { Send, Loader } from 'lucide-react'
import { generateProject } from '@/utils/api'
import { useGenerationStore } from '@/store'

/**
 * Prompt Input Component
 */
export function PromptInput() {
  const [prompt, setPrompt] = React.useState('')
  const [isLoading, setIsLoading] = React.useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const store = useGenerationStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!prompt.trim() || isLoading) return

    setIsLoading(true)
    try {
      store.startGeneration(Date.now().toString(), {})
      const result = await generateProject(prompt)

      if (result.success) {
        store.updateStatus('completed', 'Project generation complete')
        if (result.project_dir) {
          store.setProjectDir(result.project_dir)
        }
      } else {
        store.setError(result.error || 'Generation failed')
      }
    } catch (error: any) {
      store.setError(error.message || 'Failed to start generation')
    } finally {
      setIsLoading(false)
      setPrompt('')
    }
  }

  const autoResize = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'
    }
  }

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={prompt}
            onChange={(e) => {
              setPrompt(e.target.value)
              autoResize()
            }}
            placeholder="Describe your project. Example: Create me a jewelry website with product catalog, shopping cart, and checkout..."
            className="w-full px-4 py-3 bg-slate-800 text-white border border-slate-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none max-h-40"
            rows={3}
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          disabled={!prompt.trim() || isLoading}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
        >
          {isLoading ? (
            <>
              <Loader className="w-4 h-4 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Generate Project
            </>
          )}
        </button>

        <p className="text-xs text-slate-400 text-center">
          The AI will generate a complete, runnable project with frontend, backend, and database
        </p>
      </form>
    </div>
  )
}

/**
 * Project Specification Display
 */
export function ProjectSpecDisplay({ spec }: { spec: any }) {
  if (!spec) return null

  return (
    <div className="space-y-4 bg-slate-800 p-4 rounded-lg border border-slate-700">
      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Project Type</h3>
        <p className="text-white">{spec.project_type}</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-1">Frontend</h3>
          <p className="text-white">{spec.frontend}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-1">Backend</h3>
          <p className="text-white">{spec.backend}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-1">Database</h3>
          <p className="text-white">{spec.database}</p>
        </div>
      </div>

      {spec.features && spec.features.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-2">Features</h3>
          <div className="flex flex-wrap gap-2">
            {spec.features.map((feature: string, idx: number) => (
              <span
                key={idx}
                className="px-3 py-1 bg-slate-700 text-slate-200 text-xs rounded-full"
              >
                {feature}
              </span>
            ))}
          </div>
        </div>
      )}

      {spec.pages && spec.pages.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-2">Pages</h3>
          <div className="flex flex-wrap gap-2">
            {spec.pages.map((page: string, idx: number) => (
              <span key={idx} className="px-2 py-1 bg-blue-900 text-blue-200 text-xs rounded">
                {page}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
