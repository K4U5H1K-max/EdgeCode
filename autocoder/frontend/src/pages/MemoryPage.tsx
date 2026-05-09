import React from 'react'
import { useSharedMemory } from '@/hooks/useGeneration'

/**
 * Memory Page - View shared memory state
 */
export default function MemoryPage() {
  const { memory, loading } = useSharedMemory()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-slate-400">Loading memory...</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Shared Memory State</h2>

        {memory && (
          <div className="space-y-4">
            {/* Project Info */}
            {memory.project_id && (
              <div>
                <h3 className="text-sm font-semibold text-slate-300 mb-2">Project ID</h3>
                <p className="font-mono text-xs bg-slate-900 p-3 rounded text-slate-300 break-all">
                  {memory.project_id}
                </p>
              </div>
            )}

            {/* Status */}
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-2">Status</h3>
              <p
                className={`px-3 py-1 rounded-full w-fit text-sm ${
                  memory.status === 'completed'
                    ? 'bg-green-900 text-green-200'
                    : memory.status === 'error'
                    ? 'bg-red-900 text-red-200'
                    : 'bg-blue-900 text-blue-200'
                }`}
              >
                {memory.status}
              </p>
            </div>

            {/* Full Memory JSON */}
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-2">Full Memory JSON</h3>
              <pre className="bg-slate-900 p-4 rounded text-xs text-slate-300 overflow-auto max-h-96 border border-slate-700">
                {JSON.stringify(memory, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
